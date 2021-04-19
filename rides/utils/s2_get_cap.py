import s2sphere as s2

class GetCap():

    earth_radius = 6371000

    def find_cover(self, radius, center):
        radian = radius/self.earth_radius
        angle = s2.Angle(radians=radian)
        cap = s2.Cap.from_axis_angle(s2.LatLng.from_degrees(center[0], center[1]).to_point(), angle=angle)
        return cap
    
    def has(self, loc, region):
        cell = s2.Cell.from_lat_lng(s2.LatLng.from_degrees(loc[0], loc[1]))
        return region.contains(cell)


# center = [12.900067258814248, 77.65216342465733]
# cp = GetCap()
# region = cp.find_cover(1000, center)
# print(cp.cn([12.9235, 77.6521], region))