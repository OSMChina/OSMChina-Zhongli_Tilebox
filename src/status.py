class TileStatus:
    status_text=""
    # Valid status
    # -1: Initialized in martix, but not defined how to treat.
    # 0: Unvisited
    # 1: Visited, and successful created a file
    # 2: Visited, successful created a file, but maybe destroyed for some reason
    # 3: Visited, but failed to create a file
    # 4: Be asked not to visit

    def __init__(self,status_text):
        this.status_text=status_text

    def get_status_text(self):
        return self.status_text

    def set_status_text(self,status_text):
        self.status_text=status_text
