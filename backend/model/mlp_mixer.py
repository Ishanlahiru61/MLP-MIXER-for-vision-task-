import torch
import torch.nn as nn

class MlpMixer(nn.Module):
    def __init__(self, image_size=64, patch_size=16, in_channels=3, num_classes=2, dim=128, depth=4):
        super(MlpMixer, self).__init__()
        assert image_size % patch_size == 0, "Image dimensions must be divisible by patch size"
        self.num_patches = (image_size // patch_size) ** 2
        patch_dim = in_channels * patch_size * patch_size

        # Patch embedding
        self.to_patch_embedding = nn.Linear(patch_dim, dim)

        # Mixer layers
        self.mixer_layers = nn.ModuleList([])
        for _ in range(depth):
            self.mixer_layers.append(nn.ModuleList([
                # Token-mixing
                nn.Sequential(
                    nn.LayerNorm(self.num_patches),  # Fixed: normalize across tokens
                    nn.Linear(self.num_patches, self.num_patches),
                    nn.GELU(),
                    nn.Linear(self.num_patches, self.num_patches),
                ),
                # Channel-mixing
                nn.Sequential(
                    nn.LayerNorm(dim),
                    nn.Linear(dim, dim),
                    nn.GELU(),
                    nn.Linear(dim, dim),
                )
            ]))

        self.layer_norm = nn.LayerNorm(dim)
        self.fc = nn.Linear(dim, num_classes)

    def forward(self, x):
        B, C, H, W = x.shape
        patch_size = H // int(self.num_patches ** 0.5)  # compute patch size from num_patches
        patches = x.unfold(2, patch_size, patch_size).unfold(3, patch_size, patch_size)
        patches = patches.contiguous().view(B, C, -1, patch_size, patch_size)
        patches = patches.view(B, -1, C * patch_size * patch_size)

        x = self.to_patch_embedding(patches)  # shape: [B, num_patches, dim]

        for token_mixer, channel_mixer in self.mixer_layers:
            # Token-mixing: transpose to [B, dim, num_patches]
            x = x + token_mixer(x.transpose(1, 2)).transpose(1, 2)
            # hannel-mixing: [B, num_patches, dim]
            x = x + channel_mixer(x)

        x = self.layer_norm(x.mean(dim=1))
        return self.fc(x)



# Test the MLP-Mixer

if __name__ == "__main__":
    print("MLP-Mixer script started")
    x = torch.randn(2, 3, 64, 64)
    model = MlpMixer(image_size=64, patch_size=16, in_channels=3, num_classes=2, dim=128, depth=4)
    out = model(x)
    print("Output shape:", out.shape)
