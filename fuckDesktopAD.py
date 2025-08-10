import guestfs


def get_input_path(prompt):
    path = input(prompt)
    while not os.path.exists(path):
        print("路径不存在，请重新输入。")
        path = input(prompt)
    return path


vdi_path = get_input_path("你的.vdi文件路径: ")
g = guestfs.GuestFS()
g.add_drive_opts(vdi_path, format="vdi", readonly=0)
g.launch()

roots = g.inspect_os()
if not roots:
    raise RuntimeError("未找到操作系统分区")
root = roots[0]
mount_points = g.inspect_get_mountpoints(root)
system_mount = None
for mount, path in mount_points:
    if path == "/system":
        system_mount = mount
        break

if not system_mount:
    raise RuntimeError("未找到/system分区")
g.mount(system_mount, "/")

build_prop_path = "/system/build.prop"
if not g.is_file(build_prop_path):
    raise RuntimeError("未找到build.prop文件")

content = g.read_file(build_prop_path).decode("utf-8")
if not content.endswith("\n"):
    content += "\n"
content += "ro.build.version.overseas=true\n"
g.write(build_prop_path, content.encode("utf-8"))

g.sync()
g.umount_all()
g.close()
print("build.prop 已修改完成")
