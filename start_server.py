from c1c0_scheduler import server
from c1c0_scheduler.c1c0.system import C1C0System
from c1c0_scheduler.c1c0.config import DEBUG_INFO

if __name__ == '__main__':
    server.run(C1C0System(**DEBUG_INFO))

