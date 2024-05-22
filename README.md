# E-commerce Auction Site 

## Overview

This project is an e-commerce application for an auction site, developed as part of the CS50 course. Users can create auction listings, place bids, comment on listings, and manage a watchlist of interesting items. The site features dynamic listings, user authentication, and category-based item browsing.

## Features

### Models
- **User**: Extends the default Django user model.
- **Auction Listing**: Contains information about each auction item including title, description, starting bid, image URL, category, and current status (active or closed).
- **Bid**: Tracks bids placed by users on auction listings including the bid amount and the user who placed the bid.
- **Comment**: Stores comments made by users on auction listings.
- **Watchlist**: Keeps track of auction listings that users have added to their watchlist.

### Functionalities
1. **Create Listing**: 
    - Users can create new auction listings by providing a title, description, starting bid, optional image URL, and category.

2. **Active Listings Page**:
    - Displays all active auction listings with their title, description, current price, and image if available.

3. **Listing Page**:
    - Shows detailed information about a specific listing.
    - Users can add or remove the listing from their watchlist.
    - Users can place bids on the listing if it is active.
    - Listing creators can close the auction, determining the highest bidder as the winner.
    - Users can add comments to the listing.

4. **Watchlist**:
    - Users can view and manage listings they are interested in.

5. **Categories**:
    - Users can browse listings by category.

6. **Django Admin Interface**:
    - Administrators can manage all listings, bids, and comments.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Ayushma00/e-commerce-application.git
   ```

2. **Navigate to the project directory:**
   ```sh
   cd auction-site
   ```

3. **Create a virtual environment:**
   ```sh
   python -m venv env
   ```

4. **Activate the virtual environment:**
   - On Windows:
     ```sh
     .\env\Scripts\activate
     ```
   - On MacOS/Linux:
     ```sh
     source env/bin/activate
     ```

5. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

6. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

7. **Create a superuser for the admin interface:**
   ```sh
   python manage.py createsuperuser
   ```

8. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## Usage

1. **Home Page**: View all active listings.
2. **Create Listing**: Create a new auction listing by filling out the form.
3. **Listing Details**: Click on any listing to view its details, place bids, comment, or add to the watchlist.
4. **Watchlist**: Manage your watchlist by adding or removing listings.
5. **Categories**: Browse listings by categories.
6. **Admin Interface**: Administrators can manage listings, bids, and comments through the Django admin interface.

## Models

### User
Extends the `AbstractUser` model provided by Django.

### Auction Listing
- **seller**: `ForeignKey(User)` - The user who created the listing.
- **title**: `CharField(max_length=100)` - The title of the listing.
- **description**: `TextField` - Detailed description of the item.
- **category**: `CharField(max_length=3, choices=CATEGORY)` - Category of the item.
- **price**: `DecimalField(max_digits=11, decimal_places=2)` - The current price of the listing.
- **image**: `URLField` - URL for an image of the item.
- **published_date**: `DateTimeField(auto_now_add=True)` - The date the listing was published.
- **close_bid**: `BooleanField(default=False)` - Status of the listing (active/closed).

### Bid
- **auction**: `ForeignKey(AuctionListing)` - The listing on which the bid is placed.
- **user**: `ForeignKey(User)` - The user who placed the bid.
- **bid_price**: `DecimalField(max_digits=11, decimal_places=2)` - The bid amount.
- **bid_date**: `DateTimeField(auto_now_add=True)` - The date the bid was placed.

### Comment
- **auction**: `ForeignKey(AuctionListing)` - The listing on which the comment is made.
- **user**: `ForeignKey(User)` - The user who made the comment.
- **comments**: `TextField` - The text of the comment.
- **time**: `DateTimeField(auto_now_add=True)` - The time the comment was made.

### Watchlist
- **auction**: `ForeignKey(AuctionListing)` - The listing added to the watchlist.
- **seller**: `ForeignKey(User)` - The user who added the listing to the watchlist.

## Django Admin Management

- **Listings**: View, add, edit, and delete listings.
- **Bids**: View, add, edit, and delete bids.
- **Comments**: View, add, edit, and delete comments.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- CS50 Course Material: [CS50x 2021](https://cs50.harvard.edu/x/2021/)
- Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Bootstrap for styling: [https://getbootstrap.com/](https://getbootstrap.com/)

## Contact

For any inquiries or feedback, please contact [your-email@example.com].
