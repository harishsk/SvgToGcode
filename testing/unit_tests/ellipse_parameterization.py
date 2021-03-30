import math

from svg_to_gcode.geometry import Vector
from svg_to_gcode.formulas import center_to_endpoint_parameterization
from svg_to_gcode.formulas import endpoint_to_center_parameterization as endpoint_to_center_parameterization

from svg_to_gcode import TOLERANCES


def to_svg(start, end, radii, rotation, large_arc_flag, sweep_flag):
    return f"M {start.x} {start.y} A {radii.x} {radii.y} {rotation} {large_arc_flag} {sweep_flag} {end.x} {end.y}"


# center parametrization
arc = "why_not"
if arc == "simple":
    center = Vector(100, 100)
    radii = Vector(20, 60)
    rotation = 0
    start_angle = 0
    sweep_angle = math.pi
elif arc == "edge":
    center = Vector(100.0, 93.00145787776235)
    radii = Vector(70, 10)
    rotation = 0
    start_angle = 2.366399280279432
    sweep_angle = 4.691979400210515
elif arc == "dudler":
    radii = Vector(50, 10)
    rotation = math.radians(95)
    radii, center, start_angle, sweep_angle = endpoint_to_center_parameterization(
        Vector(50, 100), Vector(50, 50), radii, rotation, 1, 1)
elif arc == "why":
    radii = Vector(50, 20)
    rotation = math.radians(0)
    radii, center, start_angle, sweep_angle = endpoint_to_center_parameterization(
        Vector(50, 50), Vector(150, 50), radii, rotation, 1, 0)
elif arc == "why_not":
    center = Vector(50, 20)
    radii = Vector(100.0, 50.0)
    rotation = 0
    start_angle = -3
    sweep_angle = 3
else:
    center = Vector(100, 100.0)
    radii = Vector(50, 50)
    rotation = math.radians(90)
    start_angle = math.radians(0)
    sweep_angle = math.radians(270)

# end-pint parametrization
start, end, large_arc_flag, sweep_flag = center_to_endpoint_parameterization(center, radii, rotation, start_angle,
                                                                             sweep_angle)

radii_, center_, start_angle_, sweep_angle_ = endpoint_to_center_parameterization(start, end, radii, rotation,
                                                                                  large_arc_flag, sweep_flag)
same_radii = abs(radii - radii_) < TOLERANCES["operation"]
same_center = abs(center - center_) < TOLERANCES["operation"]
same_start_angle = abs(start_angle - start_angle_) < TOLERANCES["operation"]
same_sweep_angle = abs(sweep_angle - sweep_angle_) < TOLERANCES["operation"]

if same_radii and same_center and same_start_angle and same_sweep_angle:
    print("Identical arcs. Parametrization conversion works correctly")
else:
    print("Different arcs. Parametrization conversion is broken!")

print("original (center):", radii, center, start_angle, sweep_angle)
print("final (center):", radii_, center_, start_angle_, sweep_angle_)
print("middle (endpoint):", start, end, large_arc_flag, sweep_flag)
print("middle (svg):", to_svg(start, end, radii, math.degrees(rotation), large_arc_flag, sweep_flag))

