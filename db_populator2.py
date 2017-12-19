from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup2 import Base, Category, Item

engine = create_engine('sqlite:///catalog2.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()





# Items for Baseball
category1 = Category(name="Baseball")

session.add(category1)
session.commit()

Item1 = Item(name="Jersey", description="A jersey for baseball...",
              category=category1)

session.add(Item1)
session.commit()

Item2 = Item(name="Pants", description="Pants for baseball...",
              category=category1)

session.add(Item2)
session.commit()

Item3 = Item(name="Shoes", description="Shoes for baseball",
              category=category1)

session.add(Item3)
session.commit()

Item4 = Item(name="Gloves", description="Leather gloves for baseball",
              category=category1)

session.add(Item4)
session.commit()

Item5 = Item(name="Bat", description="A baseball bat is a smooth wooden or metal club used in baseball to hit the ball after it is thrown by the pitcher. Regulations limit it to a max of 2.75 inches in diameter at the thickest part and a max length of  42 inches. ",
              category=category1)

session.add(Item2)
session.commit()

Item6 = Item(name="Ball", description="Ball with a hard center wrapped in string and covered in leather ",
              category=category1)

session.add(Item6)
session.commit()





# Items for Basketball
category2 = Category(name="Basketball")

session.add(category2)
session.commit()

Item1 = Item(name="Jersey", description=" A breathable tank top jersey for greater ease of movement and moisture wicking",
              category=category2)

session.add(Item1)
session.commit()

Item5 = Item(name="Shorts", description="Breathable jersey shorts for greater ease of movement and moisture wicking",
              category=category2)

session.add(Item5)
session.commit()

Item5 = Item(name="Shoes", description="Shoes with ankle support and good traction for the demands of the game",
              category=category2)

session.add(Item5)
session.commit()

Item5 = Item(name="Balls", description="Balls of all sizes from small children's size all the way up to NBA regulation",
              category=category2)

session.add(Item5)
session.commit()






# Items for Football
category3 = Category(name="Football")

session.add(category3)
session.commit()

Item1 = Item(name="Jersey", description="The best jersyes from little peewees to xxxl",
              category=category3)

session.add(Item1)
session.commit()

Item2 = Item(name="Pants", description="Form fitting pants that show all the sest stains you want.",
              category=category3)

session.add(Item2)
session.commit()

Item3 = Item(name="Helmet", description="Protect your dome with the newest styles of brain buckets.",
              category=category3)

session.add(Item3)
session.commit()

Item4 = Item(name="Pads", description="Help keep your body in working order for another week, get the best pads here. ",
              category=category3)

session.add(Item4)
session.commit()

Item5 = Item(name="Socks", description="Just as high and just as great as the other football socks.",
              category=category3)

session.add(Item5)
session.commit()

Item6 = Item(name="Shoes", description="Get the best footing for hard cuts, the lightest weight for the best speed down the sideline, and you have yorself the makings of a classic. ",
              category=category3)

session.add(Item6)
session.commit()

Item7 = Item(name="Balls", description="Arnold's head shaped balls that are great for thowing. Best served without Angelica. ",
              category=category3)

session.add(Item7)
session.commit()

Item8 = Item(name="Gloves", description="Gloves used to skirt the rules. Use them and you're a cheat; don't, and you're not on the radar. Good luck. ",
              category=category3)

session.add(Item8)
session.commit()






# Items for Tennis
category4 = Category(name="Tennis")

session.add(category4)
session.commit()

Item1 = Item(name="Shirts", description="A lightweight moisture wicking shirt that allows for great range of motion.",
              category=category4)

session.add(Item1)
session.commit()

Item2 = Item(name="Shorts", description="Lightweight shorts for ease of movement",
              category=category4)

session.add(Item2)
session.commit()

Item3 = Item(name="Shoes", description="Shoes for the multiple surfaces played on",
              category=category4)

session.add(Item3)
session.commit()

Item4 = Item(name="Rackets", description="Get the best rackets from leisurely weekend palyers to the pros",
              category=category4)

session.add(Item4)
session.commit()

Item5 = Item(name="Balls", description=" ",
              category=category4)

session.add(Item5)
session.commit()

Item6 = Item(name="Wristbands", description=" ",
              category=category4)

session.add(Item6)
session.commit()







# Items for Soccer
category5 = Category(name="Soccer")

session.add(category5)
session.commit()

Item1 = Item(name="Jersey", description=" ",
              category=category5)

session.add(Item1)
session.commit()

Item2 = Item(name="Shorts", description=" ",
              category=category5)

session.add(Item2)
session.commit()

Item3 = Item(name="Socks", description=" ",
              category=category5)

session.add(Item3)
session.commit()

Item4 = Item(name="Shinguards", description=" ",
              category=category5)

session.add(Item4)
session.commit()

Item5 = Item(name="Shoes", description=" ",
              category=category4)

session.add(Item5)
session.commit()

Item6 = Item(name="Balls", description=" ",
              category=category4)

session.add(Item6)
session.commit()






# Items for Golf
category6 = Category(name="Golf")

session.add(category6)
session.commit()

Item1 = Item(name="Shirts", description=" ",
              category=category6)

session.add(Item1)
session.commit()

Item2 = Item(name="Pants", description=" ",
              category=category6)

session.add(Item2)
session.commit()

Item3 = Item(name="Shorts", description=" ",
              category=category6)

session.add(Item3)
session.commit()

Item4 = Item(name="Clubs", description=" ",
              category=category6)

session.add(Item4)
session.commit()

Item5 = Item(name="Balls", description=" ",
              category=category6)

session.add(Item5)
session.commit()

Item6 = Item(name="Gloves", description=" ",
              category=category6)

session.add(Item6)
session.commit()

Item7 = Item(name="Bags", description=" ",
              category=category6)

session.add(Item7)
session.commit()

Item8 = Item(name="Accessories", description=" ",
              category=category6)

session.add(Item8)
session.commit()








# Items for Snowboarding
category7 = Category(name="Snowboarding")

session.add(category7)
session.commit()

Item1 = Item(name="Jackets", description="Hit the slopes in the best jackets on the market. From lightweight pull-overs to the heavy duty jackets that will keep you warm in the coldest conditions. ",
              category=category7)

session.add(Item1)
session.commit()

Item2 = Item(name="Pants", description="Whether you want to hit the park right outside the lodge or try your hand at the back country., all the options are here",
              category=category7)

session.add(Item2)
session.commit()

Item3 = Item(name="Gloves", description=" ",
              category=category7)

session.add(Item3)
session.commit()

Item4 = Item(name="Socks", description=" ",
              category=category7)

session.add(Item4)
session.commit()

Item5 = Item(name="Helmets", description="Don't break your bucket and add a layer of protection for the most important part of your body",
              category=category7)

session.add(Item5)
session.commit()

Item6 = Item(name="Goggles", description=" ",
              category=category7)

session.add(Item6)
session.commit()

Item7 = Item(name="Snowbaords", description=" ",
              category=category7)

session.add(Item7)
session.commit()

Item8 = Item(name="Boots", description=" ",
              category=category7)

session.add(Item8)
session.commit()

Item9 = Item(name="Bindings", description=" ",
              category=category7)

session.add(Item9)
session.commit()





# Items for Skateboarding
category8 = Category(name="Skateboarding")

session.add(category7)
session.commit()

Item1 = Item(name="Skateboards", description="Complete boards already assembled and ready to thrash. Got everything from wider set ups for better stability at speed and smoother carving to smaller set ups best for hitting up your favorite spot with the feel and control you want.",
              category=category8)

session.add(Item1)
session.commit()

Item2 = Item(name="Decks", description="Decks of all shapes and sizes. Versatile 7-ply maple for hitting up park, vert, or local spots. ",
              category=category8)

session.add(Item2)
session.commit()

Item3 = Item(name="Trucks", description="Heavy and tough to light and controllable. Skateboard trucks of all sizes and styles and materials. ",
              category=category8)

session.add(Item3)
session.commit()

Item4 = Item(name="Wheels", description="Gotta get a good set of wheels on your board. Go soft and get that extra grip for carving or go harder for better durability. ",
              category=category8)

session.add(Item4)
session.commit()

Item5 = Item(name="Bearings", description="Get he best bearings for your ",
              category=category8)

session.add(Item5)
session.commit()

Item6 = Item(name="Shoes", description=" ",
              category=category8)

session.add(Item6)
session.commit()

Item7 = Item(name="Accessories", description=" ",
              category=category8)

session.add(Item7)
session.commit()







print "Added categories and items!"
