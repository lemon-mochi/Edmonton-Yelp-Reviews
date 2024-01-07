CREATE TRIGGER insertTip
ON tip
AFTER INSERT
AS
IF NOT EXISTS (select * from review, inserted
where inserted.business_id = review.business_id and inserted.user_id = review.user_id)
BEGIN
RAISERROR ('Can only tip after review the business.', 10, 0)
ROLLBACK TRANSACTION;
RETURN
END;