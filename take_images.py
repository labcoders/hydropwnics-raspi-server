import subprocess as sub

p = sub.Popen(['fswebcam', '/srv/http/images/cur_image.jpg'], stdout=sub.PIPE,stderr=sub.PIPE)
output, errors = p.communicate()

print(output)
print(errors)
