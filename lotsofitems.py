from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Item, Category, Base, User

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


category1 = Category(name="Soccer")
session.add(category1)
session.commit()

item1 = Item(name="Soccer Cleats", description="""Cleats are short and made
of rubber metal cleats are not allowed.""", category=category1)
session.add(item1)
session.commit()

item2 = Item(name="Shine Guards", description="""Thin guards help reduce the
chance of injury to the shin tibia, the third-most likely area of the body
to be injured playing soccer,.""", category=category1)
session.add(item2)
session.commit()

category2 = Category(name="Basketball")
session.add(category2)
session.commit()


item1 = Item(name="Shoes", description="""One needs specialized shoes when
playing basketball. It should be able to give better support to the ankle as
compared to running shoes.""", category=category2)
session.add(item1)
session.commit()

item2 = Item(name="Shine Guards", description="""The hoop or basket is a
horizontal metallic rim, circular in shape. This rim is attached to a ne
and helps one score a point.""", category=category2)
session.add(item2)
session.commit()


category3 = Category(name="Baseball")
session.add(category3)
session.commit()

item1 = Item(name="Batting Helmet", description="""A helmet protects a baseball
player if a ball accidentally hits him in the head. Some pitcher's can throw a
baseball as fast as 100 miles per hour (161 kph), so a player needs to wear a
helmet to prevent severe head injuries.""", category=category3)
session.add(item1)
session.commit()

item2 = Item(name="Batting Glove", description="""Although not a required piece
of equipment, many batters wear gloves to protect their hands while batting.
Blisters may be caused by not wearing batting gloves.
Some players wear thesegloves while running bases to protect
their hands while sliding into """, category=category3)
session.add(item2)
session.commit()


category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

item1 = Item(name="The ultimate Bag", description="""The Ultimate is getting
increasingly popular their are multiple small companies forming. One of those
companies just created the Ultimate Ultimate-Frisbee bag and tried funding it
on kickstarter, fortunately for them they raised 900% more than their initial
goal and this project came to life.
This bag can fit up to two pairs of cleats and can carry two discs
in specifically designed compartments.""", category=category4)
session.add(item1)
session.commit()

item2 = Item(name="Tripod Stool", description=""""Whoever invented this,
I think I love you. This nifty little product is a tiny stool that is
easily carried and fits in most duffle bags. When unfolded it acts as a
surprisingly comfortable place to sit. It may look a little weird to sit
on at first but your crotch is meant to straddle one of the three nylon
supports and your legs cover 2 of the 3 lower areas..""", category=category4)
session.add(item2)
session.commit()

category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()


item1 = Item(name="Altimeters", description="""Altimeters You can determine
the height of the mountain you are boarding off. Gauge how fast you can fly
down the mountain. Challenge your personal limits. Go beyond your comfort
zone..""", category=category5)
session.add(item1)
session.commit()

item2 = Item(name="Beanins and Hats", description=""""Beanies and Hats Protect
the nog from wind and chill, and look cool at the same time. Part of your
snowboard apparel. There are plenty of types to choose from. My suggestion ,
go for woolen or woolen synthetic fiber blend, as they are best insulators
. More on the use of fabrics for ski apparel """, category=category5)
session.add(item2)
session.commit()

category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

item1 = Item(name="Softshell jacket", description=""" A softshell jacket
can also serve as a midlayer, but is even more useful as it can also be
worn as a shell in less extreme conditions. These light, breathable jackets
will repel wind or light precipitation and are far more breathable than their
waterproof bretheren. Patagonia Guide, Houdini and Traverse jackets are great
examples.""", category=category6)
session.add(item1)
session.commit()

item2 = Item(name="Shine Guards", description="""TNeck collars are often worn
by linebackers and
defensive lineman for whiplash protection.""", category=category6)
session.add(item2)
session.commit()

category7 = Category(name="Football")
session.add(category7)
session.commit()


item1 = Item(name="Helmet", description="""As you would probably suspect,
the helmet is the most important piece of equipment in football.
Face masks are mandatory, a visor is optional. Jaw pads can also be worn
attached to the bottom of the helmet and provide some protection against
concussions.""", category=category7)
session.add(item1)
session.commit()

item2 = Item(name="Shine Guards", description="""TNeck collars are often worn
by linebackers and defensive
lineman for whiplash protection.""", category=category7)
session.add(item2)
session.commit()

category8 = Category(name="Skating")
session.add(category8)
session.commit()

item1 = Item(name="Knee pad", description="""Knee pads should be fitted to be
warn over clothing at practice to prevent knee holes in garments. Competitive
skaters often wear skin suits with integrated pads or keep pads that can be
worn under the suit.""", category=category8)
session.add(item1)
session.commit()

item2 = Item(name="Protective Gloves", description="""Skaters must wear
protective gloves made to protect against palm and backhand laceration from
sharp skate blades. Baseball batting gloves and other sportswear glove are
acceptable. Fingertip durability is a consideration as skaters often make left
hand finger tip contact with the ice.""", category=category8)
session.add(item2)
session.commit()


category9 = Category(name="Hockey")
session.add(category9)
session.commit()

item1 = Item(name="Hockey pants", description="""Yes they are called hockey pants,
even though they look more like shorts. The Pants protect from the knees up
to the belly. """, category=category9)
session.add(item1)
session.commit()

item2 = Item(name="Hockey bag", description="""The hoop or basket is a
horizontal metallic rim, circular in shape. This rim is attached to a net
and helps one score a pointself.The bag is used to carry all the items listed
above. There are different sizes available and also wheeled hockey bags and
non-wheeled hockey bags.""", category=category9)
session.add(item2)
session.commit()


print("Addes new items")
