## update: fix admixture issue

## usage: python ms.py demofile population_configurations migration_matrix demographic_events

import sys
import msprime
import math

demofile = sys.argv[1]
exec(open(demofile).read())
if (sys.argv[2]!= 'population_configurations'):
  population_configurations = globals()[sys.argv[2]]
  del globals()[sys.argv[2]]

if (sys.argv[3]!= 'migration_matrix'):
  migration_matrix = globals()[sys.argv[3]]
  del globals()[sys.argv[3]]

if (sys.argv[4]!= 'demographic_events'):
  demographic_events = globals()[sys.argv[4]]
  del globals()[sys.argv[4]]

Ne = 10000

# Make sure that we have a sample size of at least 2 so that we can
# initialise the simulator.
sample_size = None
if population_configurations is None:
   sample_size = 2
else:
   saved_sample_sizes = [pop_config.sample_size for pop_config in population_configurations]
   for pop_config in population_configurations:
       pop_config.sample_size = 2

def almost_equal(a, b, rel_tol=1e-9, abs_tol=0.0):
  return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def scaled_rate(m):
  return 4 * Ne * m

def scaled_time(t):
  return t / float(4 * Ne)

def scaled_size(x):
  return x / float(Ne)

abs_tol = 1e-9
demographic_events = sorted(demographic_events, key=lambda e: e.time)
simulator=msprime.simulator_factory(Ne=Ne,
            population_configurations=population_configurations,
            migration_matrix=migration_matrix,
            demographic_events=demographic_events)

ll_sim =simulator.create_ll_instance()
N = simulator.num_populations
n = saved_sample_sizes
print('--structure ' + str(N) + ' ' + ' '.join(map(str, n)))

config_index = 1
for config in simulator.population_configurations:
  initial_size = scaled_size(config.initial_size)
  growth_rate = scaled_rate(config.growth_rate)
  print("--population-size " + str(config_index) + " " + str(initial_size))
  if(growth_rate !=0):
    print("--population-growth-rate-change " + "0 " + str(config_index) + " " + str(growth_rate))
  config_index += 1

ma = []
for row in simulator.migration_matrix:
  for rate in row:
    if rate==0:
      ma.append('x')
    else:
      ma.append(str(scaled_rate(rate)))

print('--migration-matrix ' + ' '.join(ma))

start_time = 0
end_time = 0
event_index = 0
ma0 = ma
while not math.isinf(end_time):
    events = []
    while (event_index < len(demographic_events) and almost_equal(demographic_events[event_index].time,start_time, abs_tol=abs_tol)):
        events.append(demographic_events[event_index])
        event_index += 1
    for event in events:
        assert almost_equal(event.time, start_time, abs_tol=abs_tol)
        scaled_event_time = scaled_time(event.time)
        scaled_event_time_plus1 = scaled_time(event.time+1)
        if ('source' in dir(event) and 'dest' in dir(event)):
          if (event.proportion==1):
            print('--population-split ' + str(scaled_event_time) + ' ' + str(event.source+1) + ' ' + str(event.dest+1))
          if (event.proportion<1):
            print('--migration-matrix-entry-change ' + str(scaled_event_time) + ' ' + str(event.source+1) + ' ' + str(event.dest+1) + ' ' + str(event.proportion))
            print('--migration-matrix-entry-change ' + str(scaled_event_time_plus1) + ' ' + str(event.source+1) + ' ' + str(event.dest+1) + ' 0') 
        if ('initial_size' in dir(event) and event.initial_size is not None):
          print ('--population-size-change ' + str(scaled_event_time) + ' ' + str(event.population+1) + ' ' + str(event.initial_size/float(Ne)))
        if ('growth_rate' in dir(event) and event.growth_rate is not None):
          print ('--population-growth-rate-change ' + str(scaled_event_time) + ' ' + str(event.population+1) + ' ' + str(event.growth_rate))
    end_time = ll_sim.debug_demography()
    m = ll_sim.get_migration_matrix()
    N = ll_sim.get_num_populations()
    new_ma = [[m[j * N + k] for j in range(N)] for k in range(N)]
    ma_list = []
    for row in new_ma:
      for rate in row:
        if rate==0:
          ma_list.append('x')
        else:
          ma_list.append(str(scaled_rate(rate)))
    if (ma_list!=ma0):
      print('--migration-matrix-change ' + str(scaled_time(start_time)) + ' ' + str(N) + ' ' + ' '.join(ma_list))
      ma0=ma_list
    start_time = end_time
