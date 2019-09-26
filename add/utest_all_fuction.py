import unittest


# В моей программе приемущественно представлены вспомоготельные процедуры, нежели возвращающие что-либо функции.
# Здесь представлены тесты немногочисленных функций (немного видоизмененных для комфортного прописывания тестов).

def is_page_uploaded(m, frames_op_memory, page_number):
    i = m - 1
    while i > -1:
        if frames_op_memory[i][0] == page_number:
            print('Page', page_number, 'already uploaded!')
            for i in range(len(frames_op_memory)):
                print(frames_op_memory[i][0], end=' ')
            print()
            return None
        i -= 1
    return -1


def are_any_free_frames(m, frames_op_memory):
    for i in range(m):
        if frames_op_memory[i][0] == 0:
            return i
    return -1


def clearing_of_frame_lru(frames_op_memory, recent_page_uses):
    for i in range(len(frames_op_memory)):
        if frames_op_memory[i][0] not in recent_page_uses:
            replaceable_page = i
            break
    return replaceable_page


def clearing_of_frame_opt(frames_op_memory, remain_query_sequence):
    for i in range(len(frames_op_memory)):
        if remain_query_sequence.count(frames_op_memory[i][0]):
            frames_op_memory[i][1] = remain_query_sequence.index(frames_op_memory[i][0]) + 1
    for i in range(len(frames_op_memory)):
        if frames_op_memory[i][1] == 0:
            never_used_page_again = i
            return never_used_page_again
    max_using_range = 0
    for i in frames_op_memory:
        if i[1] > max_using_range:
            max_using_range = i[1]
    for i in range(len(frames_op_memory)):
        if frames_op_memory[i][1] == max_using_range:
            longest_unused_page = i
            return longest_unused_page


class IsPageUploadedTest(unittest.TestCase):
    def test_1(self):
        self.assertAlmostEqual(is_page_uploaded(4, [[1, 0], [2, 0], [3, 0], [0, 0]], 2), None)

    def test_2(self):
        self.assertAlmostEqual(is_page_uploaded(4, [[1, 0], [2, 0], [3, 0], [0, 0]], 4), -1)

    def test_3(self):
        self.assertAlmostEqual(is_page_uploaded(4, [[1, 0], [2, 0], [3, 0], [4, 0]], 5), -1)

    def test_4(self):
        self.assertAlmostEqual(is_page_uploaded(4, [[8, 0], [2, 0], [6, 0], [7, 0]], 6), None)


class AreAnyFreeFramesTest(unittest.TestCase):
    def test_5(self):
        self.assertAlmostEqual(are_any_free_frames(4, [[0, 0], [0, 0], [0, 0], [0, 0]]), 0)

    def test_6(self):
        self.assertAlmostEqual(are_any_free_frames(4, [[1, 0], [2, 0], [3, 0], [0, 0]]), 3)

    def test_7(self):
        self.assertAlmostEqual(are_any_free_frames(4, [[4, 0], [1, 0], [8, 0], [9, 0]]), -1)

    def test_8(self):
        self.assertAlmostEqual(are_any_free_frames(4, [[2, 0], [6, 0], [8, 0], [5, 0]]), -1)


class ClearingOfFrameLRUTest(unittest.TestCase):
    def test_9(self):
        self.assertAlmostEqual(clearing_of_frame_lru([[3, 0], [1, 0], [4, 0], [8, 0]], [3, 1, 8]), 2)

    def test_10(self):
        self.assertAlmostEqual(clearing_of_frame_lru([[12, 0], [2, 0], [32, 0], [8, 0]], [12, 8, 2]), 2)

    def test_11(self):
        self.assertAlmostEqual(clearing_of_frame_lru([[99, 0], [1, 0], [2, 0], [3, 0]], [3, 1, 2]), 0)

    def test_12(self):
        self.assertAlmostEqual(clearing_of_frame_lru([[13, 0], [37, 0], [14, 0], [88, 0]], [13, 14, 37]), 3)


class ClearingOfFrameOPTTest(unittest.TestCase):
    def test_13(self):
        self.assertAlmostEqual(clearing_of_frame_opt([[3, 0], [1, 0], [4, 0], [8, 0]], [2, 5, 4, 8, 1, 1]), 0)

    def test_14(self):
        self.assertAlmostEqual(clearing_of_frame_opt([[9, 0], [11, 0], [7, 0], [2, 0]], [1, 4, 3, 2, 11, 7]), 0)

    def test_15(self):
        self.assertAlmostEqual(clearing_of_frame_opt([[5, 0], [8, 0], [7, 0], [6, 0]], [5, 6, 2, 8, 7]), 2)

    def test_16(self):
        self.assertAlmostEqual(clearing_of_frame_opt([[9, 0], [1, 0], [3, 0], [4, 0]], [9, 1, 7, 6, 3, 4, 4, 2]), 3)


if __name__ == '__main__':
    unittest.main()
