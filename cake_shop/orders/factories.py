from .models import Cake, Decoration


class BaseCakeFactory:
    def create(self, user, validated_data, decorations):
        cake = Cake.objects.create(
            user=user,
            base=validated_data['base'],
            cream=validated_data['cream'],
            filling=validated_data['filling'],
            size=validated_data['size'],
            shape=validated_data['shape'],
            price_type=validated_data['price_type']
        )

        if decorations:
            cake.decorations.set(decorations)
        else:
            self.apply_defaults(cake)

        return cake

    def apply_defaults(self, cake):
        pass


class CandyCakeFactory(BaseCakeFactory):
    def apply_defaults(self, cake):
        defaults = Decoration.objects.filter(
            name__in=[
                'Посыпка',
                'Шоколадная глазурь',
                'Кондитерская посыпка'
            ]
        )
        cake.decorations.set(defaults)


class PremiumCakeFactory(BaseCakeFactory):
    def apply_defaults(self, cake):
        premium = Decoration.objects.filter(
            name__in=[
                'Золотая пудра',
                'Серебряная пудра',
                'Стразы'
            ]
        )
        cake.decorations.set(premium)


def get_factory(cake_type):
    if cake_type == 'candy':
        return CandyCakeFactory()
    elif cake_type == 'premium':
        return PremiumCakeFactory()
    return BaseCakeFactory()