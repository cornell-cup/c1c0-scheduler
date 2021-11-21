import threading
import unittest

from c1c0_scheduler import utils


DEBUG = False
# DEBUG = True


class UtilsTest(unittest.TestCase):

    def test_reader_writer_basic(self):
        # noinspection PyPep8Naming
        N = 1000
        read_write_suite = utils.ReaderWriterSuite()
        d = {
            'a': 0
        }

        def reader(d_):
            with read_write_suite.reader():
                b = d_['a']
                if DEBUG:
                    print(f'Read: {b}')
                return b

        def writer(d_):
            with read_write_suite.writer():
                b = d_['a']
                b += 1
                if DEBUG:
                    print(f'Wrote1: {d["a"]}')
                d['a'] = b

        readers = [
            threading.Thread(target=reader, args=(d,)) for _ in range(N)]

        writers = [
            threading.Thread(target=writer, args=(d,)) for _ in range(N)]

        for i in range(N):
            readers[i].start()
            writers[i].start()

        for i in range(N):
            readers[i].join()
            writers[i].join()
        if DEBUG:
            print(f'Ended test_reader_writer_basic with {d["a"]}')
        self.assertEqual(d['a'], N)

    def test_reader_writer_adv(self):
        # noinspection PyPep8Naming
        N = 1000
        read_write_suite = utils.ReaderWriterSuite()
        d = {
            'a': 0
        }

        def reader1(d_):
            with read_write_suite.reader():
                b = d_['a']
                if DEBUG:
                    print(f'Read1: {b}')
                return b

        def reader2(d_):
            with read_write_suite.reader():
                b = d_['a']
                if DEBUG:
                    print(f'Read2: {b}')
                return b

        def writer1(d_):
            with read_write_suite.writer():
                b = d_['a']
                b += 1
                if DEBUG:
                    print(f'Wrote1: {d["a"]}')
                d['a'] = b

        def writer2(d_):
            with read_write_suite.writer():
                b = d_['a']
                b -= 1
                if DEBUG:
                    print(f'Wrote2: {d_["a"]}')
                d_['a'] = b

        readers1 = [
            threading.Thread(target=reader1, args=(d,)) for _ in range(N)]
        readers2 = [
            threading.Thread(target=reader2, args=(d,)) for _ in range(N)]

        writers1 = [
            threading.Thread(target=writer1, args=(d,)) for _ in range(N)]
        writers2 = [
            threading.Thread(target=writer2, args=(d,)) for _ in range(N)]

        for i in range(N):
            readers1[i].start()
            writers1[i].start()
            readers2[i].start()
            writers2[i].start()

        for i in range(N):
            readers1[i].join()
            writers1[i].join()
            readers2[i].join()
            writers2[i].join()

        if DEBUG:
            print(f'Ended test_reader_writer_adv with {d["a"]}')
        self.assertEqual(d['a'], 0)


if __name__ == '__main__':
    unittest.main()
