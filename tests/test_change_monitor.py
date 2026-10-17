import subprocess
import sys
import unittest
from pathlib import Path
from change_monitor.demo import observe


class LastGoodBaseline(unittest.TestCase):
    def test_initial(self):
        self.assertEqual(observe(None,200,b"x")[0],"initial")

    def test_unchanged(self):
        _, h = observe(None,200,b"x")
        self.assertEqual(observe(h,200,b"x"),("unchanged",h))

    def test_changed(self):
        _, h = observe(None,200,b"x")
        state, new = observe(h,200,b"y")
        self.assertEqual(state,"changed")
        self.assertNotEqual(h,new)

    def test_failure_preserves_baseline(self):
        _, h = observe(None,200,b"x")
        for code, content in [(None,None),(403,b"denied"),(500,b"error"),(304,None),(200,None)]:
            with self.subTest(code=code):
                self.assertEqual(observe(h,code,content),("unavailable",h))
        self.assertEqual(observe(h,200,b"x"),("unchanged",h))

    def test_empty_success_is_not_failure(self):
        self.assertEqual(observe(None,200,b"")[0],"initial")

    def test_invalid_content_type(self):
        with self.assertRaises(TypeError):
            observe(None,200,"not bytes")

    def test_failure_exit_code(self):
        script = Path(__file__).resolve().parents[1] / "change_monitor/demo.py"
        p = subprocess.run([sys.executable,str(script),"--simulate-failure"],capture_output=True,text=True)
        self.assertEqual(p.returncode,2)
        self.assertEqual(p.stdout.strip(),"unavailable")

    def test_demo(self):
        script = Path(__file__).resolve().parents[1] / "change_monitor/demo.py"
        p = subprocess.run([sys.executable,str(script)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0)
        self.assertEqual(p.stdout.splitlines(),["initial","unchanged","unavailable","unchanged","changed","changed"])
