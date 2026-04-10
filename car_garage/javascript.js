/* -------------------- HERO IMAGE SLIDER -------------------- */
const hero = document.querySelector(".hero");

const images = [
    "https://images.unsplash.com/photo-1542362567-b07e54358753",
    "https://images.unsplash.com/photo-1552519507-da3b142c6e3d",
    "https://images.unsplash.com/photo-1515923162065-719b3e0b166c",
    "https://images.unsplash.com/photo-1502877338535-766e1452684a",
    "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023"
];

let idx = 0;

setInterval(() => {
    hero.style.background = `url('${images[idx]}') center/cover no-repeat`;
    idx = (idx + 1) % images.length; 
}, 500);

/* -------------------- POPUP OPEN -------------------- */
function openPayment(){
    document.getElementById("paymentPopup").style.display = "flex";
}

/* -------------------- BOOKING FORM -------------------- */
document.getElementById("bookingForm").addEventListener("submit", function(e){
    e.preventDefault();
    openPayment();
});

/* -------------------- POPUP CLOSE -------------------- */
function closePopup(){
    document.getElementById("paymentPopup").style.display = "none";
}

/* -------------------- DEFAULT RATING = 4.5 -------------------- */
const stars = document.querySelectorAll("#starContainer span");
const msg = document.getElementById("ratingMsg");

function setDefaultRating(){
    stars.forEach(star => star.classList.remove("active"));
    for(let i=0; i<4; i++){
        stars[i].classList.add("active");
    }
    stars[4].style.color = "#ff9800a0";
}
setDefaultRating();

/* -------------------- USER CLICK RATING -------------------- */
stars.forEach(star => {
    star.addEventListener("click", () => {
        const rating = star.getAttribute("data-id");

        stars.forEach(s => { 
            s.classList.remove("active");
            s.style.color = "#555";
        });

        for(let i=0; i<rating; i++){
            stars[i].classList.add("active");
            stars[i].style.color = "#ff9800";
        }

        msg.innerText = `Thank you! You rated ${rating} ★`;
    });
});