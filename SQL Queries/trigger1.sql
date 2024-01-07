CREATE TRIGGER updateReviewsBusiness
ON review
AFTER INSERT
AS BEGIN
update business
set review_count =
(select count(*)
from review
where
(select max(date) max_date
from review r
where r.user_id = review.user_id and business_id = inserted.business_id
group by user_id) = review.date),
stars =
(select AVG(CAST(review.stars AS DECIMAL(2,1)))
from review
where
(select max(date) max_date
from review r
where r.user_id = review.user_id and business_id = inserted.business_id
group by user_id) = review.date)
from business, inserted
where business.business_id = inserted.business_id
END;