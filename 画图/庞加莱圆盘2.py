import math
import numpy as np

import drawsvg as draw
from drawsvg import Drawing
from hyperbolic import euclid
from hyperbolic.poincare import *
from hyperbolic.poincare.util import (
    radial_euclid_to_poincare, triangle_side_for_angles,
)
import hyperbolic.tiles as htiles


class TileDecoratorFish(htiles.TileDecoratorPolygons):
    def __init__(self, p1=4, p2=3, q=3):
        """
        修改后使 q=2 时也可以适用的示例。
        """
        self.p1 = p1
        self.p2 = p2
        self.q = q

        theta1 = math.pi * 2 / p1
        theta2 = math.pi * 2 / p2
        phi_sum = math.pi * 2 / q

        # 若 q=2，则 phi_sum = π，角度和会造成双曲几何三角形失效，
        # 这里演示一个最简单可行的处理：把中间角设得极小，让它还处于双曲几何区域。
        # 或者也可以直接跳过第三块多边形的放置。
        if q == 2:
            # 用一个非常小的角度替代 phi_sum/2，以避免三角失效
            tiny_angle = 1e-8
            r1 = triangle_side_for_angles(theta1 / 2, tiny_angle, theta2 / 2)
            r2 = triangle_side_for_angles(theta2 / 2, tiny_angle, theta1 / 2)
        else:
            r1 = triangle_side_for_angles(theta1 / 2, phi_sum / 2, theta2 / 2)
            r2 = triangle_side_for_angles(theta2 / 2, phi_sum / 2, theta1 / 2)

        t_gen1 = htiles.TileGen.make_regular(p1, hr=r1)
        t_gen2 = htiles.TileGen.make_regular(p2, hr=r2)

        # 这里开始对摆放进行区分
        t1 = t_gen1.centered_tile()
        t2 = t_gen2.placed_against_tile(t1, side=-1)

        if q == 2:
            # 如果 q=2，只用两块多边形相交，不放置 t3
            point_base = t2.vertices[-1]
        else:
            # 原有的逻辑
            t3 = t_gen1.placed_against_tile(t2, side=-1)
            point_base = t3.vertices[-1]

        # 旋转出一圈鱼鳍顶点，用于构造外边的 Hypercycle 轮廓
        points = [Transform.rotation(deg=-i * 360 / p1).apply_to_point(point_base)
                  for i in range(p1)]
        vertices = t1.vertices

        # 用 Hypercycle 连顶点
        edges = []
        for i, point in enumerate(points):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % p1]
            edge = Hypercycle.from_points(*v1, *v2, *point, segment=True, exclude_mid=True)
            edges.append(edge)
        edge_poly = Polygon(edges=edges, vertices=vertices)

        # 内部“鱼肚子”区域形状
        origin = Point(0, 0)
        corner = Point.from_h_polar(r1, theta=0)
        corner2 = Transform.rotation(rad=-theta1).apply_to_point(corner)

        if q == 2:
            # 只构造三角形
            poly = Polygon.from_vertices((origin, corner, corner2))
        else:
            # 原始的四边形
            center = Point.from_h_polar(r2, theta=-math.pi + phi_sum / 2)
            center = Transform.translation(corner).apply_to_point(center)
            poly = Polygon.from_vertices((origin, corner, center, corner2))

        desc = poly.make_restore_points()
        descs = [Transform.rotation(deg=-i * 360 / p1).apply_to_list(desc)
                 for i in range(p1)]

        super().__init__(edge_poly, poly_descs=descs)
        self.colors = ['#ffbf00', 'green', 'red', 'blue', 'gray', 'brown']

    def to_drawables(self, tile=None, layer=0, **kwargs):
        if tile is None:
            trans = Transform.identity()
            # 对应最初的“开始瓷砖”
            codes = range(self.p1)
        else:
            trans = tile.trans
            codes = [side.code[1] for side in tile.sides]
        polys = [Polygon.from_restore_points(trans.apply_to_list(desc))
                 for desc in self.poly_descs]
        ds = []
        # layer 0: 内部色块
        if layer == 0:
            for i, poly in enumerate(polys[1:]):
                color = self.colors[codes[i] % len(self.colors)]
                d = poly.to_drawables(fill=color, opacity=0.5, **kwargs)
                ds.extend(d)
        # layer 1: 最外面一圈（白色）
        if layer == 1:
            d_last = polys[0].to_drawables(hwidth=0.03, fill='white', **kwargs)
            ds.extend(d_last)
        # layer 2: 边框（黑色）
        if layer == 2:
            for i, poly in enumerate(polys[1:]):
                d = poly.to_drawables(hwidth=0.01, fill='black', **kwargs)
                ds.extend(d)
        return ds


class TileLayoutFish(htiles.TileLayout):
    def calc_gen_index(self, code):
        """Override in subclass to control which type of tile to place."""
        if code == 0 or code == 1:
            return code
        index, color, cw = code
        return index

    def calc_tile_touch_side(self, code, gen_index):
        """Override in subclass to control tile orientation."""
        return 0

    def calc_side_codes(self, code, gen_index, touch_side, default_codes):
        """Override in subclass to control tile side codes."""
        p = len(default_codes)
        if code == 0 or code == 1:
            c = (code + 1) % 2
            # 简单示例写法，可按自身需求修改
            if p % 2 == 0:
                return ((c, 0, 1), (c, 1, 0)) * (p // 2)
            else:
                return ((c, 0, 1), (c, 1, 2), (c, 2, 0)) * (p // 3)
        index, color, other_color = code
        c = (index + 1) % 2
        if index == 1:
            new_colors = {
                             (0, 1): (0, 2, 3),
                             (1, 0): (1, 3, 2),
                             (0, 2): (0, 3, 1),
                             (2, 0): (2, 1, 3),
                             (0, 3): (0, 1, 2),
                             (3, 0): (3, 2, 1),
                             (1, 2): (1, 0, 3),
                             (2, 1): (2, 3, 0),
                             (1, 3): (1, 2, 0),
                             (3, 1): (3, 0, 2),
                             (2, 3): (2, 0, 1),
                             (3, 2): (3, 1, 0),
                         }[(color, other_color)] * 10
        elif index == 0:
            new_colors = {
                             (0, 1): (0, 3, 0, 3),
                             (1, 2): (1, 3, 1, 3),
                             (2, 0): (2, 3, 2, 3),
                             (0, 2): (0, 1, 0, 1),
                             (2, 3): (2, 1, 2, 1),
                             (3, 0): (3, 1, 3, 1),
                             (0, 3): (0, 2, 0, 2),
                             (3, 1): (3, 2, 3, 2),
                             (1, 0): (1, 2, 1, 2),
                             (1, 3): (1, 0, 1, 0),
                             (3, 2): (3, 0, 3, 0),
                             (2, 1): (2, 0, 2, 0),
                         }[(color, other_color)] * 10
        else:
            assert False
        new_colors = new_colors[:p]
        codes = [(c, new_color, new_colors[(i + 1) % len(new_colors)])
                 for i, new_color in enumerate(new_colors)]
        return codes


if __name__ == '__main__':
    p1 = 4
    p2 = 3
    q = 2  # 这里改成2进行测试
    rotate = 0
    depth = 5

    theta1 = math.pi * 2 / p1
    theta2 = math.pi * 2 / p2
    phi_sum = math.pi * 2 / q
    # 若 q=2, 下述三角形参数在双曲几何中会退化
    # 因此在 TileDecoratorFish 内部做了判断

    # 两种生成器
    # skip=1 表示顶点连接跳一个顶点(可根据需求调整或去掉skip)
    t_gen1 = htiles.TileGen.make_regular(p1, hr=0.5, skip=1)
    t_gen2 = htiles.TileGen.make_regular(p2, hr=0.5, skip=1)

    decorator1 = TileDecoratorFish(p1, p2, q)

    t_layout = TileLayoutFish()
    # 初始的“发生器”，给它指定侧码等
    t_layout.add_generator(t_gen1, ((0, 1) * 10)[:p1], decorator1)
    t_layout.add_generator(t_gen2, ((0, 1, 2) * 10)[:p2], htiles.TileDecoratorNull())

    start_tile = t_layout.start_tile(code=0, rotate_deg=-rotate)
    tiles = t_layout.tile_plane(start_tile, depth=depth)

    d = Drawing(2, 2, origin='center')
    d.draw(euclid.Circle(0, 0, 1), fill='silver')
    for tile in tiles:
        d.draw(tile, layer=0)
    for tile in tiles:
        d.draw(tile, layer=1)
    for tile in tiles:
        d.draw(tile, layer=2)

    d.set_render_size(w=400)
    d.save_svg('escherApprox_q2.svg')
    d.rasterize(to_file='escherApprox_q2.png')
