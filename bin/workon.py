#!/opt/bin/python
import os, sys
projects = [x for x in os.listdir('/volume1/moindev/.env') \
		if os.path.isdir(os.path.join('/volume1/moindev/.env', x))]


if __name__ == "__main__":
	# print sys.argv, projects, os.listdir('/volume1/moindev/.env')
	if len(sys.argv) != 2:
		print "\n".join(projects)
	else:
		project = sys.argv[1]
		print os.path.join('/volume1/moindev/.env', project, 'bin', 'activate')
