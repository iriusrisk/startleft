from vsdx import Shape

from slp_visio.slp_visio.load.strategies.component.component_identifier_strategy import ComponentIdentifierStrategy


class ComponentIdentifier:

    @staticmethod
    def is_component(shape: Shape) -> bool:
        for strategy in ComponentIdentifierStrategy.get_strategies():
            if strategy.is_component(shape):
                return True

        return False
