#!/usr/bin/env python
# encoding: utf-8
# vim: sw=4 ts=4 expandtab ai smartindent
#
# @author: Francesco Vozza <fvozza@gmail.com>
#
# Copyright (c) 2010 by Francesco Vozza
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA

import os, os.path, sys, re 

__desc__ = "Simple tool to match .srt file to corresponding .avi in a given dir"
__version__ = "0.1"

def usage():
	print "Usage: %s <dir>" % sys.argv[0]
	exit(1)

def episode(name):
	"""Returns a tuple: (season, episode) """
	s = re.search(r'.*[sS](?P<season>\d+)[eE](?P<episode>\d+).*', name)
	if not s:
		return
	return (s.group('season'), s.group('episode'))

def main():
	if len(sys.argv) == 1:
		usage()
	
	subs_dir = sys.argv[1]
	
	if not os.path.isdir(subs_dir):
		print "%s is not a directory" % subs_dir
		exit(1)
	
	all_files = os.listdir(subs_dir)

	videos = [v for v in all_files if re.match(r'.*\.avi', v)]
	subs = [s for s in all_files if re.match(r'.*\.srt', s)]

	# episodes = ( (season, episode), (video_name, ext), (sub_name, ext) )
	episodes = []
	for v in videos:
		ev = episode(v)
		for s in subs:
			if episode(s) == ev:
				episodes.append((ev, os.path.splitext(v), os.path.splitext(s)))
	
	for e in episodes:
		old_name = e[2][0]+e[2][1]
		new_name = e[1][0]+e[2][1]
		
		if os.path.exists(os.path.join(subs_dir, new_name)):
			print 'S%sE%s : [SKIP] %s exists' % (e[0][0], e[0][1], new_name)
			continue

		try:
			os.rename(os.path.join(subs_dir, old_name), os.path.join(subs_dir, new_name))
			print 'S%sE%s : %s --> %s' % (e[0][0], e[0][1], old_name, new_name)
		except OSError, ex:
			print 'S%sE%s : %s' % (e[0][0], ex)

if __name__ == '__main__':
    sys.exit(main())