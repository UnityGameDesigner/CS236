import torch
import torch.nn as nn
import torch.nn.functional as F

class DISCEMO(nn.Module):
    def __init__(self, debug=False):
        super(DISCEMO, self).__init__()
        self.drp_rate = 0

        self.filters = [(64, 3, 2), (128, 3, 2), (256, 3, 2), (512, 3, 2), (512, 3, 2)]

        prev_filters = 3
        for i, (num_filters, filter_size, stride) in enumerate(self.filters):
            setattr(self, 
                    'conv_'+str(i+1), 
                    nn.Sequential(
                    nn.Conv2d(prev_filters, num_filters, kernel_size=filter_size, stride=stride, padding=filter_size//2),
                    nn.LeakyReLU(0.3)
                )
            )
            prev_filters = num_filters

        self.projector = nn.Sequential(
            nn.Linear(4608, 2048),
            nn.LeakyReLU(0.3),
            nn.Linear(2048, 512)
        )

        # Transformer
        transformer_layer = nn.TransformerEncoderLayer(d_model=512, nhead=8)
        self.transformer_encoder = nn.TransformerEncoder(transformer_layer, num_layers=6)

        self.cls = nn.Sequential(
            nn.Linear(512, 6)
        )

        # Optimizer
        self.opt = torch.optim.Adam(list(self.parameters()), lr = 1e-06, betas=(0.5, 0.999))
        self.scheduler = torch.optim.lr_scheduler.StepLR(self.opt, 150, gamma=0.1, last_epoch=-1)

    def forward(self, video):
        x = video
        n, c, t, w, h = x.size(0), x.size(1), x.size(2), x.size(3), x.size(4)
        x = x.contiguous().view(t * n, c, w, h)
        
        for i in range(len(self.filters)):
            x = getattr(self, 'conv_'+str(i+1))(x)
        h = x.view(n, t, -1)
        h = self.projector(h)
    
        h = h.permute(1, 0, 2)  # Reshape for transformer (S, N, E)
        h = self.transformer_encoder(h)

        h_class = self.cls(h[-1, :, :])  # Use last token for classification
    
        return h_class

    def enableGrad(self, requires_grad):
        for p in self.parameters():
            p.requires_grad_(requires_grad)
