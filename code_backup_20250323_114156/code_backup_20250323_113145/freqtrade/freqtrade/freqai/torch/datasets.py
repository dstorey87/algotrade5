# REMOVED_UNUSED_CODE: import torch


# REMOVED_UNUSED_CODE: class WindowDataset(torch.utils.data.Dataset):
# REMOVED_UNUSED_CODE:     def __init__(self, xs, ys, window_size):
# REMOVED_UNUSED_CODE:         self.xs = xs
# REMOVED_UNUSED_CODE:         self.ys = ys
# REMOVED_UNUSED_CODE:         self.window_size = window_size
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __len__(self):
# REMOVED_UNUSED_CODE:         return len(self.xs) - self.window_size
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __getitem__(self, index):
# REMOVED_UNUSED_CODE:         idx_rev = len(self.xs) - self.window_size - index - 1
# REMOVED_UNUSED_CODE:         window_x = self.xs[idx_rev : idx_rev + self.window_size, :]
# REMOVED_UNUSED_CODE:         # Beware of indexing, these two window_x and window_y are aimed at the same row!
# REMOVED_UNUSED_CODE:         # this is what happens when you use :
# REMOVED_UNUSED_CODE:         window_y = self.ys[idx_rev + self.window_size - 1, :].unsqueeze(0)
# REMOVED_UNUSED_CODE:         return window_x, window_y
