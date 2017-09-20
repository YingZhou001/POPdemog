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

## change sample size to 1
for config in population_configurations:
  config.sample_size = 1

def almost_equal(a, b, rel_tol=1e-9, abs_tol=0.0):
  return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def scaled_time_to_generations(Ne, t):
  return 4 * Ne * t

abs_tol = 1e-9
demographic_events = sorted(demographic_events, key=lambda e: e.time)
simulator=msprime.simulator_factory(Ne=Ne,
            population_configurations=population_configurations,
            migration_matrix=migration_matrix,
            demographic_events=demographic_events)
ll_sim =simulator.create_ll_instance()
N = simulator.get_num_populations()
n = simulator.get_sample_configuration()
Ne = simulator._effective_population_size
print('--structure ' + str(N) + ' ' + ' '.join(map(str, n)))

config_index = 1
for config in simulator.get_population_configurations():
  initial_size = config.initial_size/float(Ne)
  growth_rate = config.growth_rate * 4 *Ne
  print("--population-size " + str(config_index) + " " + str(initial_size))
  if(growth_rate !=0):
    print("--population-growth-rate-change " + "0 " + str(config_index) + " " + str(growth_rate))
  config_index += 1

ma = []
for row in simulator.get_scaled_migration_matrix():
  for rate in row:
    if rate==0:
      ma.append('x')
    else:
      ma.append(str(rate))

print('--migration-matrix ' + ' '.join(ma))

start_time = 0
scaled_end_time = 0
event_index = 0
ma0 = ma
while not math.isinf(scaled_end_time):
    events = []
    while (event_index < len(demographic_events) and almost_equal(demographic_events[event_index].time,start_time, abs_tol=abs_tol)):
        events.append(demographic_events[event_index])
        event_index += 1
    #if len(events) > 0:
    #    print("Events @ generation {}".format(start_time))
    for event in events:
        assert almost_equal(event.time, start_time, abs_tol=abs_tol)
        scaled_event_time = float(event.time)/(4*Ne)
        if ('source' in dir(event) and 'destination' in dir(event)):
          if (event.proportion==1):
            print('--population-split ' + str(scaled_event_time) + ' ' + str(event.source+1) + ' ' + str(event.destination+1))
          if (event.proportion<1):
            print('--admixture ' + str(scaled_event_time) + ' ' + str(event.source+1) + ' ' + str(event.proportion))
        if ('initial_size' in dir(event) and event.initial_size is not None):
          print ('--population-size-change ' + str(scaled_event_time) + ' ' + str(event.population_id+1) + ' ' + str(event.initial_size/float(Ne)))
        if ('growth_rate' in dir(event) and event.growth_rate is not None):
          print ('--population-growth-rate-change ' + str(scaled_event_time) + ' ' + str(event.population_id+1) + ' ' + str(event.growth_rate))
        #print(event)
    scaled_end_time = ll_sim.debug_demography()
    end_time = scaled_time_to_generations(Ne,scaled_end_time)
    m = ll_sim.get_migration_matrix()
    N = ll_sim.get_num_populations()
    new_ma = [
        [m[j * N + k] / (4 * Ne) for j in range(N)] for k in range(N)]
    ma_list = []
    for row in new_ma:
      for rate in row:
        if rate==0:
          ma_list.append('x')
        else:
          ma_list.append(str(rate*4*Ne))
    if (ma_list!=ma0):
      print('--migration-matrix-change ' + str(start_time/float(4*Ne)) + ' ' + str(N) + ' ' + ' '.join(ma_list))
      ma0=ma_list
    start_time = end_time
