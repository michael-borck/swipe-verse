from typing import Any, Dict

import flet as ft


# Note: For Flet 0.27.x compatibility
# We're using a standard class instead of UserControl which is only in newer Flet versions
class ResourceBar:
    """
    A visual indicator for game resources that displays their levels using icons
    with a fill indicator rather than numeric values.
    """

    def __init__(
        self,
        resources: Dict[str, int],
        resource_icons: Dict[str, str],
        max_resources: Dict[str, int], # Add max_resources parameter
        **kwargs: Any,
    ) -> None:
        self.resources = resources
        self.resource_icons = resource_icons
        self.max_resources = max_resources
        self.resource_controls: Dict[str, ft.Tooltip] = {}

    def build(self) -> ft.Row:
        """Build the resource bar with all the resource indicators"""
        resources_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10)

        for resource_id, value in self.resources.items():
            if resource_id not in self.resource_icons:
                continue

            # Create the resource indicator
            icon_control = self._create_resource_icon(resource_id, value)
            resources_row.controls.append(icon_control)
            self.resource_controls[resource_id] = icon_control

        return resources_row

    def _create_resource_icon(self, resource_id: str, value: int) -> ft.Tooltip:
        """
        Create a visual indicator for a resource using fill level instead of numbers.
        """
        icon_path = self.resource_icons[resource_id]

        # The filled (colored) version
        filled_icon = ft.Image(
            src=icon_path, width=50, height=50, fit=ft.ImageFit.CONTAIN
        )

        # The dark-tint depletion overlay - positioned at the top
        # and clipped based on the depleted amount
        depletion_height = (self.max_resources[resource_id] - value) / self.max_resources[resource_id] * 50
        depletion_overlay = ft.Container(
            content=ft.Image(
                src=icon_path,
                width=50,
                height=50,
                color=ft.colors.BLACK, # Use black tint
                color_blend_mode=ft.BlendMode.DARKEN, # Blend mode to apply tint
                opacity=0.6, # Adjust opacity for tint effect
                fit=ft.ImageFit.CONTAIN,
            ),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            # Clip from the bottom based on the depleted amount
            height=depletion_height,
            alignment=ft.alignment.top_center,
        )

        # Stack the filled version and the depletion overlay
        icon_stack = ft.Stack(
            controls=[filled_icon, depletion_overlay], width=50, height=50
        )

        # Add a tooltip showing the resource name
        return ft.Tooltip(message=resource_id.capitalize(), content=icon_stack)

    def update_resource(self, resource_id: str, new_value: int) -> None:
        """Update a specific resource with a new value"""
        if resource_id not in self.resource_controls:
            return

        # Update the stored value
        self.resources[resource_id] = new_value

        # Get the stack
        stack = self.resource_controls[resource_id].content

        # Update the depletion overlay height
        depletion_container = stack.controls[1] # Assuming depletion_overlay is still the second control in the stack
        depletion_container.height = (self.max_resources[resource_id] - new_value) / self.max_resources[resource_id] * 50

        # Update the control
        stack.update()

    def update_all_resources(self, resources: Dict[str, int]) -> None:
        """Update all resources with new values"""
        for resource_id, value in resources.items():
            self.update_resource(resource_id, value)
