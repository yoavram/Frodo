import qstat as q

r = q.local_qstat()
r = q.parse_qstat1(r)
r = q.summarize1(r['fields'],r['records'])
print "Total: %d\nRunning: %d\nWaiting: %d" % (r['total'], r['r'], r['qw'])
