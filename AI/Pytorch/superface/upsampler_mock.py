from AI.Pytorch.superface.enhancer_base import EnhancerBase


# Meanwhile restoring faces, it needs a separate backend to process and get a hi-resolution background
# If there is already hi-res or keep the same background, use this class to paste back to restored faces
# This steep its optional, not mandatory.
class MockUpsampler(EnhancerBase):
    def __init__(self):
        super().__init__()
        self.background = None  # Jus settle the background as you need

    # This just will return the background as you settled
    def enhance(self, img=None, outscale=None):
        if self.background is not None:
            return [self.background]
        return [img]
