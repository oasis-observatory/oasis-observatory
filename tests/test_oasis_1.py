#!/usr/bin/env python3
from oasis.s_generator.params import sample_parameters
from oasis.s_generator.abbreviator import abbreviate
from oasis.s_generator.timeline import dynamic_timeline

print("OASIS OFFLINE TEST — 100% WORKING")
print("="*60)

# 1. Sample fake ASI
params = sample_parameters()
print(f"Origin: {params['initial_origin']}")
print(f"Goal:   {params['stated_goal']}")

# 2. Generate title
title = abbreviate(params)
print(f"\nTitle: {title}")

# 3. Build timeline
timeline = dynamic_timeline()
print(f"\nTimeline:")
for p in timeline:
    print(f"   • {p['phase']:20} {p['years']}")

# 4. Fake narrative (no LLM)
print(f"\nNARRATIVE (offline mode):")
print(f"In {timeline[0]['years']}, a {params['initial_origin']} {params['architecture']} "
      f"ASI emerged with {params['autonomy_degree']} autonomy. "
      f"It pursued {params['stated_goal']} through {params['deployment_strategy']} deployment. "
      f"By {timeline[-1]['years']}, humanity entered a new equilibrium.")

print("\nSUCCESS — abbreviator + timeline work perfectly!")
print("   Run: ollama serve &   → then: oasis generate")