import unittest
from src.tracker import iou,track
class TestTracker(unittest.TestCase):
 def test_iou_and_persistent_track(self):
  self.assertEqual(iou([0,0,10,10],[0,0,10,10]),1); rows=[{"frame":0,"label":"person","x1":0,"y1":0,"x2":10,"y2":10},{"frame":1,"label":"person","x1":1,"y1":0,"x2":11,"y2":10}]; out=track(rows); self.assertEqual(out[0]["track_id"],out[1]["track_id"])
