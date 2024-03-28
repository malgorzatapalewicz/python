import math

import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, x, y): #translacja punktu
        self.x += x
        self.y += y

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def translate(self, x, y): #dokonanie translacji o dany wektor
        self.start.translate(x, y)
        self.end.translate(x, y)

    def equation(self):
        #linear general equation Ax + By + C = 0
        A = self.end.y - self.start.y
        B = self.start.x - self.end.x
        C = self.end.x * self.start.y - self.start.x * self.end.y #x2 * y1 - x1 * y2
        return A, B, C

    def point_belongs(self, point): #sprawdzenie przynaleznosci punktu do prostej
        A, B, C = self.equation() #pobranie wspolczynnikow
        return A * point.x + B * point.y + C == 0

    def point_position(self, point): # okreslenie polozenia punktu wzgledem prostej (prawo/lewo)
        A, B, C = self.equation()
        value = A * point.x + B * point.y + C
        if value > 0:
            return "prawo"
        elif value < 0:
            return "lewo"
        else:
            return "na linii"

    def reflection(self, point): #dokonanie odbicia danego punktu wzgledem linii i prostej
        A, B, C = self.equation()
        #pobranie wspolrzednych punktu ktory ma zostac odbity
        x = point.x
        y = point.y
        x_refl = x - 2 * (A * x + B * y + C) * A / (A ** 2 + B ** 2) #A^2 + B^2
        y_refl = y - 2 * (A * x + B * y + C) * B / (A ** 2 + B ** 2)
        return Point(x_refl, y_refl)

    def intersection1(line1, line2):
        #obliczenie punktu przeciecia prostych na podstawie wspolczynnikow rownania ogolnego
        A1, B1, C1 = line1.equation()
        A2, B2, C2 = line2.equation()
        if A1 * B2 - A2 * B1 == 0:
            return None #proste rownolegle
        return Point((B1 * C2 - B2 * C1) / (A1 * B2 - A2 * B1), (A2 * C1 - A1 * C2) / (A1 * B2 - A2 * B1))

    def intersection2(line1, line2):
        #obliczenie punktu przeciecia prostych na podstawie dwoch linii o znanym poczatku i koncu
        x1, y1 = line1.start.x, line1.start.y
        x2, y2 = line1.end.x, line1.end.y
        x3, y3 = line2.start.x, line2.start.y
        x4, y4 = line2.end.x, line2.end.y

        A1, B1, C1 = -y2 + y1, x2 - x1, -(y1 * (x2 - x1) - x1 * (y2 - y1))
        A2, B2, C2 = -y4 + y3, x4 - x3, -(y3 * (x4 - x3) - x3 * (y4 - y3))
        if A1 * B2 - A2 * B1 == 0:
            return None
        x = (B1 * C2 - B2 * C1) / (A1 * B2 - A2 * B1)
        y = (A2 * C1 - A1 * C2) / (A1 * B2 - A2 * B1)

        return Point(x,y)


    def distance(point, line):
        A, B, C = line.equation()
        x, y = point.x, point.y
        numerator = abs(A * x + B * y + C)
        denominator = math.sqrt(A ** 2 + B ** 2)
        distance = numerator / denominator
        return distance

class Triangle:
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    @staticmethod
    def can_form_triangle(distance, line1, line2, line3):
        if distance <= 0:
            return False

        #sprawdzenie czy odleglosc jest mniejsza od dlugosci kazdej linii
        if distance >= distance(line1.start, line1) and distance >= distance(line1.end, line1):
            return False
        if distance >= distance(line2.start, line2) and distance >= distance(line2.end, line2):
            return False
        if distance >= distance(line3.start, line3) and distance >= distance(line3.end, line3):
            return False
        return True

    def create_triangle(self, line1, line2, line3):
        if self.can_form_triangle(line1, line2, line3):
            return Triangle(line1.start, line2.start, line3.start)
        else: return None

    def display_triangle(triangle):
        if triangle:
            plt.plot([triangle.point1.x, triangle.point2.x], [triangle.point1.y, triangle.point2.y], 'c-')
            plt.plot([triangle.point2.x, triangle.point3.x], [triangle.point2.y, triangle.point3.y], 'c-')
            plt.plot([triangle.point3.x, triangle.point1.x], [triangle.point3.y, triangle.point1.y], 'c-')
            plt.plot(triangle.point1.x, triangle.point1.y, 'ko')
            plt.plot(triangle.point2.x, triangle.point2.y, 'ko')
            plt.plot(triangle.point3.x, triangle.point3.y, 'ko')
            plt.grid()
            plt.gca().set_aspect('equal', adjustable='box')
            plt.show()
        else:
            print("trojakt nie moze byc utworzony.")


#testy jednostkowe
def test():
    point1 = Point(1, 1)
    point2 = Point(4, 5)
    line1 = Line(point1, point2)

    #wizualizacja graficzna
    # k-czarny, o-punkty w ksztalcie kol, '-' oznacza linie ciagla
    #plt.plot([point1.x, point2.x], [point1.y, point2.y], 'ko-')

    # wyznaczenie rownania prostej
    #print("wspolczynniki rownania prostej:", line1.equation())

    #sprawdzenie przynaleznosci punktu do linii
    point3 = Point(2, 3)
    #print("czy punkt nalezy do linii?", line1.point_belongs(point3))
    #plt.plot(point3.x, point3.y, 'co')
    #plt.text(point3.x, point3.y, 'point 3' )

    #okreslenie polozenia punktu względem linii
     #print("Położenie punktu względem linii:", line1.point_position(point3))

    #dokonanie odbicia punktu wzgledem linii
    #reflected_point = line1.reflection(point3)
    #print("po odbiciu punktu wzgledem linii, nowe wspolrzedne wynosza:", reflected_point.x, reflected_point.y)
    #plt.plot(reflected_point.x, reflected_point.y, 'mo')

    #obliczanie punktu przeciecia
    line2 = Line(Point(1, 1), Point(4, 5))
    line3 = Line(Point(2, 3), Point(4, 2))
    intersection = line2.intersection2(line3)
    plt.plot([line2.start.x, line2.end.x], [line2.start.y, line2.end.y], 'c-', label="Linia 2")
    plt.plot([line3.start.x, line3.end.x], [line3.start.y, line3.end.y], 'm-', label="Linia 3")

    if intersection:
        plt.plot(intersection.x, intersection.y, 'ko', label="Punkt przecięcia")
        plt.text(intersection.x, intersection.y, 'Punkt przecięcia', verticalalignment='bottom')

    plt.grid() #siatka na wykresie
    plt.gca().set_aspect('equal', adjustable='box') #takie same proporcje na osiach x i y
    plt.show()
    triangle = Triangle(Point(1, 1), Point(5, 2), Point(3, 6))
    Triangle.display_triangle(triangle)


if __name__ == "__main__":
    test()
