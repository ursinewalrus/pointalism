from PIL import Image
import operator

class Painter:

    def __init__(self, point_radius, overlap, file_path, average):
        self.filename = file_path.split('/')[-1]
        self.dir = file_path.split('/')[0:-1]
        self.image = Image.open(file_path)

        self.point_radius = point_radius
        self.image_width, self.image_height = self.image.size
        self.pixels = list(self.image.getdata())

        self.points = self.create_points(overlap)
        self.rows = self.create_rows()
        self.fill_points()
        if(average):
            self.calculated_points = self.find_point_average_rgb()
        else:
            self.calculated_points = self.find_point_mean_rgb()

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
                    realX = (xi + (x - self.point_radius))
                    realY = (yi + (y - self.point_radius))
                    dx = realX - x
                    dy = realY - y
                    d_squared = (dx * dx) + (dy * dy)
                    if (d_squared <= self.point_radius * self.point_radius):
                        self.points[str(x) + "-" + str(y)].append({str(realX) + "-" + str(realY) :pix})

    def find_point_average_rgb(self):
        avg_points = {}
        for i,point in enumerate(self.points):
            avg = (0, 0, 0)
            total_points = 0
            for circle_points in self.points[point]:
                for cPixel in circle_points:
                    pixel = circle_points[cPixel]
                    avg = (avg[0] + pixel[0], avg[1] + pixel[1], avg[2] + pixel[2])
                    total_points += 1
            avg = (avg[0] / total_points, avg[1] / total_points, avg[2] / total_points)
            avg_points[point] = avg
        return avg_points

    def find_point_mean_rgb(self):
        mean_points = {}
        for i,point in enumerate(self.points):
            mean_dic = [{},{},{}]
            for circle_points in self.points[point]:
                for cPixel in circle_points:
                    pixel = circle_points[cPixel]
                    for i,val in enumerate(pixel):
                        if val in mean_dic[i]:
                            mean_dic[i][val] += 1
                        else:
                            mean_dic[i][val] = 1
            mean_colors = [0,0,0]
            for color,pixels in enumerate(mean_dic):
                mean_color = max(mean_dic[color].iteritems(), key=operator.itemgetter(1))[0]
                mean_colors[color] = mean_color
            mean_colors = (mean_colors[0],mean_colors[1],mean_colors[2])
            mean_points[point] = mean_colors
        return mean_points

    def paint_picture_with_points(self):
        im = Image.new("RGB", (self.image_width , self.image_height))
        for center in self.points:
            for point in self.points[center]:
                indices, pixel = point.popitem()
                x,y = [int(c) for c in indices.split('-')]
                im.putpixel((x,y),self.calculated_points[center])
        im.save("C:\\Users\\jkerxhalli\\Desktop\\golf\\pointalism\\pictures\\test.png")



    # def draw_pic_from_points(self):
    #     pointalism_pic = Image.new("RGB",(self.image_width,self.image_height))
