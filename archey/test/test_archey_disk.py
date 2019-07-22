"""Test module for Archey's disks usage detection module"""

import unittest
from unittest.mock import patch

from archey.entries.disk import Disk


class TestDiskEntry(unittest.TestCase):
    """
    Here, we mock the `check_output` call to disk utility tools.
    """
    @patch(
        'archey.entries.disk.check_output',
        side_effect=[
            """\
Filesystem       1GB-blocks  Used Available Use% Mounted on
/dev/mapper/root      512GB  14GB     498GB   2% /
/dev/mapper/home      512GB  47GB     465GB   9% /home
total                1024GB  61GB     963GB  11% -
""",
            FileNotFoundError()  # `btrfs` call will fail.
        ]
    )
    def test_df_only(self, _):
        """Test computations around `df` output"""
        self.assertRegex(
            Disk().value,
            r'.*61 GB.* \/ 1024 GB')

    @patch(
        'archey.entries.disk.check_output',
        side_effect=[
            """\
Filesystem       1GB-blocks  Used Available Use% Mounted on
/dev/mapper/root      512GB  14GB     498GB   2% /
/dev/mapper/home      512GB  47GB     465GB   9% /home
total                1024GB  61GB     963GB  11% -
""",
            """\
Overall:
    Device size:                1820.00GiB
    Device allocated:           1170.00GiB
    Device unallocated:          669.99GiB
    Device missing:                0.00GiB
    Used:                       1140.00GiB
    Free (estimated):            692.57GiB      (min: 692.57GiB)
    Data ratio:                       1.00
    Metadata ratio:                   1.00
    Global reserve:                0.51GiB      (used: 0.00GiB)
"""
        ]
    )
    def test_df_and_btrfs(self, _):
        """Test computations around `df` and `btrfs` outputs"""
        self.assertRegex(
            Disk().value,
            r'.*1201 GB.* \/ 2844 GB')

if __name__ == '__main__':
    unittest.main()
