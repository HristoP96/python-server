
file="test.xlsx"
responses=()
# Query first 10 posts
for postId in {0..9};
do
response=$(curl "https://api.mockaroo.com/api/c9804b80?count=1000&key=95c46f40")
responses+=($response)
done

for i in "${responses[@]}"; do echo $i >> 'customers.csv'; done
