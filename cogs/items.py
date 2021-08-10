class Item:

    def __init__(self, ref, name, emoji, image, description):
        self.items = []
        self.ref = ref
        self.name = name
        self.emoji = emoji
        self.image = image
        self.description = description

    def __repr__(self):
        return '<Item ref={0.id} name={0.name} emoji={0.emoji} image={0.image} description={0.description}>'.format(self)

    @property
    def ref(self):
        return self.ref
    @property
    def name(self):
        return self.name
    @property
    def emoji(self):
        return self.emoji
    @property
    def image(self):
        return self.image
    @property
    def description(self):
        return self.description

a=Item('a', 'Ticket', '<:infinity_ticket:874551859233325086>', 'https://cdn.discordapp.com/emojis/874551859233325086.png?v=1', 'Used to trade.')
print(f"{Item.ref}")
print(f"{type(a)} {type(Item)}")


economy_items = [ 
    {
        'id':'a',
        'name':'Ticket',
        'emoji':'<:infinity_ticket:874551859233325086>',
        'image':'https://cdn.discordapp.com/emojis/874551859233325086.png?v=1',
        'description':''
    },
    {
        'id':'b',
        'name': 'Coin',
        'emoji':'<:infinity_coin:874548715338227722>',
        'image':'https://cdn.discordapp.com/emojis/874548715338227722.png?v=1',
        'description':''
    }
                ]