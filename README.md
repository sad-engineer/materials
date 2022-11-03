# `materials`

`materials` - модуль работы с базой данных материаллов

Поддерждиваемые функции:
	
	Получение списка  доступных материалов по наименованию группы материала:
		brands = materials.by_class(any_class)
	
	Получение списка доступных материалов по индексу группы материала:
		brands = materials.by_index(any_index)

	Получение индекса, группы и подгруппы материала:
		index, class_, subclass = materials.characteristics(any_brand)

	Получение химического состава материала:
		table = materials.chem_struct(any_brand)

	Получение твердости материала:
		table_hardness = materials.hardness(any_brand)

	Получение предела прочности материала:
		table_strength = materials.tensile_strength(any_brand)
	
