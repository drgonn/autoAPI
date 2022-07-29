import os

from writefile.go_dapr.migration import write_go_dapr_mygrations



def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def write_go_dapr(p):
    """生成go dapr 后端文件"""
    print("生成go dapr 后端文件")
    # 生成目录
    path = p.app_root_dir
    mkdir(os.path.join(path, 'go_dapr'))
    mkdir(os.path.join(path, 'go_dapr/internal'))
    mkdir(os.path.join(path, 'go_dapr/internal/database'))

    migrate_path = os.path.join(path, 'go_dapr/internal/database/migrations')
    mkdir(migrate_path)
    write_go_dapr_mygrations(p, migrate_path)

    mkdir(os.path.join(path, 'go_dapr/internal/forms'))
    mkdir(os.path.join(path, 'go_dapr/internal/http'))
    mkdir(os.path.join(path, 'go_dapr/internal/repo'))



