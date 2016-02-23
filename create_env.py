import os
import re

def normalize_name(name):
    return re.sub(r'([A-Z])', r'_\1', name).replace(" ", "_").lower().strip(" \t_")

def adapt_template(data, target_root_path, path, filename, target_filename = None):
    project_name = normalize_name(data["APP_NAME"])
    if target_filename is None:
        target_filename = filename
    else:
        target_filename = target_filename.replace("@APPNAME@", project_name)

    output_str = ""
    with open(os.path.join("templates", path, filename), "r") as fd:
        output_str = fd.read()
    output_str = output_str.replace("@APPNAME@", project_name)
    output_str = output_str.replace("@VERSION@", data["APP_VERSION"])
    output_str = output_str.replace("@MAINTENER@", data["APP_MAINTENER"])
    output_str = output_str.replace("@DESCRIPTION@", data["APP_DESCRIPTION"])

    target_path = os.path.join(target_root_path, path)

    if not os.path.exists(target_path):
        os.makedirs(target_path)
    with open(os.path.join(target_path, filename), "w") as fd:
        fd.write(output_str + "\n")

if __name__ == "__main__":
    spec_data = {
            "APP_NAME" : {"value" : "", "description" : "Project name", "mandatory" : True},
            "APP_VERSION" : {"value" : "1.0.0", "description" : "Project version", "mandatory" : False},
            "APP_MAINTENER" : {"value" : "Romain CONNESSON", "description" : "Maintener", "mandatory" : False},
            "APP_DESCRIPTION" : {"value" : "", "description" : "Description", "mandatory" : False},
        }
    data_order = ["APP_NAME", "APP_VERSION", "APP_MAINTENER", "APP_DESCRIPTION"]

    data= {}
    for key in data_order:
        item = spec_data[key]
        loop = True
        while loop:
            txt = item["description"]
            if not item["mandatory"]:
                txt += ' (Default : "%s")' % item["value"]
            res = raw_input("%s : " % txt)
            if res:
                data[key] = res
                loop = False
            elif item["mandatory"]:
                print "This parameter is mandatory"
            else:
                data[key] = item["value"]
                loop = False

    files = [
        ("build/DEBIAN", "control", None),
        ("build/DEBIAN", "postinst", None),
        ("build/DEBIAN", "prerm", None),
        ("build", "Dockerfile.dev", None),
        ("build", "Dockerfile.deploy", None),
        ("build", "install_dev.sh", None),
        ("build", "install_nginx.sh", None),
        ("conf", "nginx_default.conf", None),
        ("conf", "srv.service", "@APPNAME@.service"),
        (".", "Makefile", None),
        (".", "README.md", None),
    ]

    target_root_path = "bin"
    for path, filename, target_filename in files:
        adapt_template(data, target_root_path, path, filename, target_filename)
