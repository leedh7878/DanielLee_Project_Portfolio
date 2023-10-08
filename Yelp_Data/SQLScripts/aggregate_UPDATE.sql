--Need to work on resetting '[null]' values back to 0

Update 	business
Set		numcheckins = 
(Select 	Count(cdate) As numberCheckins 
From 		checkins
Where 	checkins.business_id = business.business_id
Group By	business_id);

Update 	business
Set		numtips = 
(Select 	Count(tipdate) As numberTips 
From 		tip
Where 	tip.business_id = business.business_id
Group By	business_id);

Update 	users
Set		totallikes = 
(Select 	Sum(likes) As numberLikes 
From 		tip
Where 	tip.user_id = users.user_id
Group By	user_id);

Update 	users
Set		tipcount = 
(Select 	Count(tipdate) As tipCount 
From 		tip
Where 	tip.user_id = users.user_id
Group By	user_id);