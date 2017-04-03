    def advance_time(self):
        """parse, advance, and save time"""

        # parse time
        year = int(self.start[:4])
        month = int(self.start[5:7])
        day = int(self.start[8:10])
        hours = int(self.start[11:13])
        minutes = int(self.start[14:16])
        seconds = int(self.start[17:19])
        time = datetime.datetime(year, month, day, hours, minutes, seconds)

        # advance time
        time = time + datetime.timedelta(minutes=self.rain_interval)
        time = time.isoformat(" ")

        # timestamp
        evolved_elevation = 'elevation_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # m
        depth = 'depth_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # m
        sediment_flux = 'flux_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # kg/ms
        erosion_deposition = 'erosion_deposition_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # kg/m2s
        difference = 'difference_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # m

        return evolved_elevation, depth, sediment_flux, erosion_deposition, difference
