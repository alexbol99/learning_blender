bl_info = {
    "name": "Smallest Add-on",
    "author": "Alex Bol",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "category": "Object",
    "location": "Operator Search",
    "description": "More monkeys!",
    "warning": "",
    "doc_url": "",
    "tracker_url": ""
}


def register():
    print("Hello World")


def unregister():
    print("Goodbye addon")


if __name__ == "__main__":
    register()