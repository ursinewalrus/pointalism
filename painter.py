from PIL import Image

class Painter:

    def __init__(self, point_radius, overlap, file_path):
        self.point_radius = point_radius
        self.image = Image.open(file_path)
        self.image_width, self.image_height = self.image.size
        self.pixels = list(self.image.getdata())

        self.points = self.create_points(overlap)
        self.rows = self.create_rows()
        self.fill_points()
        a = 1

    # perhaps a different indicing scheme would be good
    def create_points(self,overlap):
        distance = 2 if overlap else 1
        points = {}
        for w in range(self.point_radius, self.image_width - self.point_radius, self.point_radius * distance):
            for h in range(self.point_radius, self.image_width - self.point_radius, self.point_radius * distance):
                points[str(w) + "-" + str(h)] = []
        return points

    def create_rows(self):
        rows = []
        for x in range(0, self.image_width * self.image_height, self.image_width):
            rows.append(self.pixels[x:x + self.image_width])
        return rows

    def fill_points(self):
        for point in self.points:
            x = int(point.split('-')[0])  # int(math.floor(index / im_width))
            y = int(point.split('-')[1])  # index % im_width
            for xi, rw in enumerate(self.rows[y - self.point_radius:min(self.image_height, y + self.point_radius)]):
                for yi, pix in enumerate(rw[x - self.point_radius:min(self.image_height, x + self.point_radius)]):
                    dx = (xi + (x - self.point_radius)) - x
                    dy = (yi + (y - self.point_radius)) - y
                    d_squared = (dx * dx) + (dy * dy)
                    if (d_squared <= self.point_radius * self.point_radius):
                        self.points[str(x) + "-" + str(y)].append(pix)

    def find_point_average_rgb(self):
        avg_points = {}
        for i,point in enumerate(self.points):
            avg = (0, 0, 0)
            total_points = 0
            for pixel in self.points[point]:
                avg = (avg[0] + pixel[0], avg[1] + pixel[1], avg[2] + pixel[2])
                total_points += 1
            avg = (avg[0] / total_points, avg[1] / total_points, avg[2] / total_points)
            avg_points[point] = avg
        return avg_points



    # def draw_pic_from_points(self):
    #     pointalism_pic = Image.new("RGB",(self.image_width,self.image_height))
