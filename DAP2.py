import pandas as pd
import numpy as np

# 1. خواندن داده‌ها
df = pd.read_csv("sales.csv")
df['product'] = df['product'].str.strip().str.lower()

# 2. ساخت ماتریس صفر و یکی
matrix = pd.crosstab(df['name'], df['product'])

# 3. تعریف خرید مشتری جدید (مثلاً فقط book خریده)
new_purchase = np.array([1, 0, 0, 0, 0])  # فرض بر اینه که ترتیب ستون‌ها: book, eraser, note, pen, pencil
new_series = pd.Series(new_purchase, index=matrix.columns)

# 4. بررسی شباهت با هر مشتری قبلی
similarity_scores = {}

for name, row in matrix.iterrows():
    match = (row.values == new_series.values)
    score = np.sum(match)  # تعداد ویژگی‌های برابر
    similarity_scores[name] = score

# 5. مرتب‌سازی بر اساس تعداد ویژگی‌های مشابه
sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

# 6. چاپ نتایج
print("میزان شباهت ساده با مشتریان قبلی (تعداد تطابق):")
for name, score in sorted_scores:
    print(f"{name}: {score} ویژگی مشابه")
# 7. ساخت سری از خرید مشتری جدید برای مقایسه
new_series = pd.Series(new_purchase, index=matrix.columns)

# 8. شبیه‌ترین مشتری‌ها (مثلاً اونایی که 4 یا 5 ویژگی مشابه داشتن)
max_match = max(similarity_scores.values())
top_customers = [name for name, score in similarity_scores.items() if score == max_match]

# 9. بررسی کالاهایی که اون مشتری‌ها خریدن و مشتری جدید هنوز نخریده
suggested_items = pd.Series(0, index=matrix.columns)

for name in top_customers:
    customer_purchases = matrix.loc[name]
    # فقط کالاهایی که مشتری مشابه خریده و مشتری جدید نخریده
    mask = (customer_purchases == 1) & (new_series == 0)
    suggested_items += mask.astype(int)

# مرتب‌سازی پیشنهادات
suggested_items = suggested_items[suggested_items > 0].sort_values(ascending=False)

print("\n پیشنهاد کالا به مشتری جدید:")
print(suggested_items)
    

