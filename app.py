from flask import Flask, redirect, request
import subprocess

app = Flask(__name__)

def get_jupyters():
  try:
    env_directory = "/home/stein/.local/share/virtualenvs/stein-rWgKSEJ6/bin" # TODO: find this in a way that works as a service
    jupyter_command = f"pipenv"
    result = subprocess.run(
      [jupyter_command, 'run', 'jupyter', 'notebook', 'list'],
      capture_output=True, 
      text=True, 
      check=True  # This will raise an exception if the command returns a non-zero exit code
    )
    server_list = result.stdout.split("\n")
    to_ret = []
    for server_string in server_list:
      if "::" not in server_string:
        continue
      url, path = server_string.split(" :: ")
      to_ret.append([path, url])
    return to_ret
  except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")
    print(e.output)
    raise e
    return [[f"error: {e}", "/"]]

@app.route('/')
def hello_world():
  jupyter_list = get_jupyters()
  if len(jupyter_list) == 0:
    return "<html><body>no jupyter servers running</body></html>"
  to_ret = ["<html><h1>active jupyter server</h1>", "<div id='link-list'>"]
  to_ret.append("""
<style>
body {
  font-size: 28px;
}
#link-list {
  display: flex;
  flex-direction: column;
}
</style>""")
  for path, url in jupyter_list:
    to_ret.append(f"<a href={url}>{path}</a>")
  to_ret.append("</div></html>")
  return ''.join(to_ret)

@app.route('/<path:subpath>')
def catch_all(subpath):
  jupyter_list = get_jupyters()
  for path, url in jupyter_list:
    if path.endswith(subpath):
      return redirect(url)
  return redirect("/")

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
