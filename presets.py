from manimlib.imports import *
from manimgui.defaults import *
from manimgui.temp import *

#real_func
#complex_func
#parametric_surface
#parametric_curve
#linear_transformation

config = {
    "R_func" : real_func,
    "C_func" : complex_func,
    "linear_transformation" : linear_transf,
    "show_basis_vects" : show_basis_vectors,
    # "parametric_surface" : lambda u, v: np.array([
    #                 1.5*np.cos(u)*np.cos(v),
    #                 1.5*np.cos(u)*np.sin(v),
    #                 1.5*np.sin(u)
    #             ]),
    # "parametric_curve" : lambda u : np.array([
    #             1.2*np.cos(u),
    #             1.2*np.sin(u),
    #             u/2
    #         ]),
    # "fourier_string" : "X"
}

class ComplexFunction(LinearTransformationScene):
    CONFIG = {
        "function" : config["C_func"],
        "show_basis_vectors" : False,
        "foreground_plane_kwargs" : {
            "x_radius" : FRAME_X_RADIUS,
            "y_radius" : FRAME_Y_RADIUS,
            "secondary_line_ratio" : 0
        },
    }
    def construct(self):
        self.setup()
        self.plane.prepare_for_nonlinear_transform(100)
        self.wait()
        self.play(ApplyMethod(
            self.plane.apply_complex_function, self.function,
            run_time = 5,
            path_arc = 0 #(originally np.pi/2)
        ))
        self.wait()

class LinearTransformation(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : config["show_basis_vects"],
        "matrix" : config["linear_transformation"]
    }
    def construct(self):
        self.setup()
        self.wait()
        self.apply_matrix(self.matrix)
        self.wait()

class SlopeAndDerivative(GraphScene):
    CONFIG = {
        "function" : config["R_func"],
        "x_min" : -6,
        "x_max" : 6,
        "x_axis_width" : FRAME_WIDTH,
        "x_labeled_nums" : list(range(-6, 7)),
        "y_min" : -35,
        "y_max" : 35,
        "y_axis_height" : FRAME_HEIGHT,
        "y_tick_frequency" : 5,
        "y_labeled_nums" : list(range(-30, 40, 10)),
        "graph_origin" : ORIGIN,
        "dx" : 0.2,
        "deriv_x_min" : -3,
        "deriv_x_max" : 3,
    }
    def construct(self):
        self.setup_axes(animate = False)
        graph = self.get_graph(self.function)
        label = self.get_graph_label(
            graph, "f(x) = x^3",
            direction = LEFT,
        )


        deriv_graph, full_deriv_graph = [
            self.get_derivative_graph(
                graph,
                color = GREEN,
                x_min = low_x,
                x_max = high_x,
            )
            for low_x, high_x in [
                (self.deriv_x_min, self.deriv_x_max),
                (self.x_min, self.x_max),
            ]
        ]
        deriv_label = self.get_graph_label(
            deriv_graph,
            "\\frac{df}{dx}(x) = 3x^2",
            x_val = -3, 
            direction = LEFT
        )
        deriv_label.shift(0.5*DOWN)

        ss_group = self.get_secant_slope_group(
            self.deriv_x_min, graph, 
            dx = self.dx,
            dx_line_color = BLACK,
            df_line_color = BLACK,
            secant_line_color = YELLOW,
        )

        self.play(ShowCreation(graph))
        self.play(Write(label, run_time = 1))
        self.wait()
        self.play(Write(deriv_label, run_time = 1))
        self.play(ShowCreation(ss_group, lag_ratio = 0))
        self.animate_secant_slope_group_change(
            ss_group,
            target_x = self.deriv_x_max,
            run_time = 10,
            added_anims = [
                ShowCreation(deriv_graph, run_time = 10)
            ]
        )
        self.play(FadeIn(full_deriv_graph))
        self.wait()
        for x_val in -2, -self.dx/2, 2:
            self.animate_secant_slope_group_change(
                ss_group,
                target_x = x_val,
                run_time = 2
            )
            if x_val != -self.dx/2:
                v_line = self.get_vertical_line_to_graph(
                    x_val, deriv_graph,
                    line_class = DashedLine
                )
                self.play(ShowCreation(v_line))
                self.play(FadeOut(v_line))



# class ParametricCurve(ThreeDScene):
#     def construct(self):
#         curve1=ParametricFunction(
#                 config["parametric_curve"],
#                 color=RED,t_min=-TAU,t_max=TAU,
#             )

#         curve1.set_shade_in_3d(True)

#         axes = ThreeDAxes()

#         self.add(axes)

#         self.set_camera_orientation(phi=80 * DEGREES,theta=-60*DEGREES)
#         self.begin_ambient_camera_rotation(rate=0.1) 
#         self.play(ShowCreation(curve1))
#         self.wait(5)

# #----- Surfaces
# class SurfacesAnimation(ThreeDScene):
#     def construct(self):
#         axes = ThreeDAxes()



#         surface = ParametricSurface(
#                 config["parametric_surface"]
#             ,v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[RED_D, RED_E],
#             resolution=(15, 32)).scale(2)


#         self.set_camera_orientation(phi=75 * DEGREES)
#         self.begin_ambient_camera_rotation(rate=0.2)

#         self.add(axes)
#         self.play(Write(surface))
#         self.wait(5)
#         self.play(FadeOut(surface))

