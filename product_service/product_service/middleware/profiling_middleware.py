import cProfile
import pstats
import cStringIO  # Use cStringIO for Python 2.7 strings
import logging
import os
import time

logger = logging.getLogger('product_service.middleware.profiling_middleware')
PROFILE_DIR = 'profiling/'  # Ensure this directory exists


class ProfilingMiddleware(object):
    def __init__(self):
        print("ProfilingMiddleware initialized")

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'profile' in request.GET:
            # print('Profiling GET parameter found')
            logger.debug("Profiling started for request: %s", request.path)
            self.pr = cProfile.Profile()

            def profiled_view(*args, **kwargs):
                self.pr.enable()
                try:
                    response = view_func(*args, **kwargs)
                finally:
                    self.pr.disable()
                return response

            response = profiled_view(request, *view_args, **view_kwargs)

            # Save profile data to a file
            # timestamp = int(time.time() * 1000)
            profile_filename = os.path.join(PROFILE_DIR, "profiling.prof")
            with open(profile_filename, 'w') as f:
                ps = pstats.Stats(self.pr, stream=f)
                ps.dump_stats(profile_filename)
            print("Profiling data saved to {}".format(profile_filename))
            logger.debug("Profiling data saved to {}".format(profile_filename))

            return response
        else:
            print('Profiling not enabled in GET parameters')
            logger.debug("Profiling not enabled for request: %s", request.path)
        return None

    def process_response(self, request, response):
        return response
