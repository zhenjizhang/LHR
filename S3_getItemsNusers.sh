awk -F, '{print $1}' /Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/item_user_rating_Video_Games.csv | sort -n | uniq | cat > /Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/items.csv
awk -F, '{print $2}' /Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/item_user_rating_Video_Games.csv | sort -n | uniq | cat > /Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/users.csv