Finance
We’ll take the concepts we’ve seen to create CS50 Finance, a virtual stock trading website with an account for users to register for, the ability to get quotes for shares of stocks and to virtually buy or sell them. We’ll also have a history page for each account to see what we’ve done in the past.
[2:45] We look at the distribution code for CS50 Finance, or the code that we’ll all start off with. We have an application.py file that our Flask app will run, with various configuration options, a connection to a database file finance.db, and routes for . This follows the MVC, Model-View-Controller, pattern, which generally separates the concerns of data and how that’s stored (our database), the views that display some amount of data (our templates), and controllers that control the logic of what is displayed when (our application.py routes).
[4:45] Since we’re using a third-party API, or Application Programming Interface, some code that someone else wrote designed for us to use, we’ll also need an API key to get stock information.
[5:30] Notice that our routes also have a @login_required decorator, or extra attribute in Python to indicate that the function should behave differently. Flask allows us to automatically redirect users to a login page, and we have the login functionality implemented in our distribution code too. The /login route checks whether a matching user and password exists in our database (for a POST method, as from the login form), or displays the login form for a GET method. And in our database, instead of storing the user’s raw password, which is more insecure since hackers might use them against other websites, we store the hash of their password which is sufficient for verification, but difficult from which to recover the original password.
[14:30] After the login route we have logout, which just clears the session, and we have quote, register, and sell routes left to implement.
[15:10] We’ll implement:
register so we can register for a new account
quote so we can get a price quote for a stock
buy to buy some shares of a stock
index to show the stocks in our account
sell to sell some shares of a stock
history to show transactions in the past
and a personal feature of our choice
[15:55] We talk about the requirements for each of these routes, and how they might be implemented with conditions based on the request’s method, and either display forms or perform some action after validating the request.
[20:50] We have an existing finance.db database, and we can use sqlite3 finance.db to run queries that add columns or tables that we might want to use to store additional data to support our routes.
[23:00] index will query our database for a user’s stocks and their cash balance, along with using an API to get the current price of each and displaying all this data with a template. sell, too, should have validation and update our data in the database.
[25:25] Finally, we might need another table (in our database) to support our history page, and display the data for each user’s transactions in a table (in our template).
[26:25] And we’ll need to add a personal touch, whether that’s allowing users to change their password, add cash, or additional features.