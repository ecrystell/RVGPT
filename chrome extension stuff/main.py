# to add content into html
from js import document  # DOM for this popup page
para = document.createElement("p")
para.innerHTML = "This is a paragraph."
para.className = "info"
document.getElementById("content").appendChild(para)


def test_func(waht): 
    print('yes' + waht)

test_func('no')


# scrape data 

# check for fake reviews -- output actual one (nicholas)

# check seller profile/reliability (fraud/no -- qian)

# compare products 
#import compare 
#compare.compare_pdts("nike jordans")