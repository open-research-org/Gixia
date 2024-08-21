# Gixia
Gixia is an open-sourced research community that promotes research openness.

Here are what will come next in our first release:
+ A platform where people can mark the paper as "Added" or "Read".
+ Once read a paper, user is asked to comment and score it from 1 to 5.
+ A review section is present for further discussion and posting.

Please stay tuned.

## About

Gixia is a product of the non-profit organization **Open Research Organization**, which is founded to promote research openness and communication among scholars all over the world. We are trying to help make paper review more transparent in the first step. It's a big revolution to the long-lasting peer-review history, but we believe we are moving to the next era.

## Build Database
Download the arXiv metadata snapshot from [Kaggle arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv/data). Import the JSON file into MongoDB. This part includes all the papers since 2008 to most recent week.

Run following scripts to incrementally retrieve newest papers. It's recommended to set the `from_date` param to several days ago because the Kaggle arXiv Dataset is updated weekly, we need to fill the gap between recent days. For deployment, we just need to schedule a daily task to run this script.
```
python update_arxiv_data.py --from_date 2024-08-16
```