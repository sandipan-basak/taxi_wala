import s2sphere as s2

class GetCap():

    earth_radius = 6371000

    def find_cover(self, radius, center):
        radian = radius/self.earth_radius
        angle = s2.Angle(radians=radian)
        cap = s2.Cap.from_axis_angle(s2.LatLng.from_degrees(center[0], center[1]).to_point(), angle=angle)
        return cap
    
    def cap_contains(self, loc, cap):
        cell = s2.Cell.from_lat_lng(s2.LatLng.from_degrees(loc[0], loc[1]))
        cell_id = cell.id()
        return cap.contains(cell_id)