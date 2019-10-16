import requests
import logging

logger=logging.getLogger(__name__)

def report_score(teamID,teamName,score):
  logger.debug(
    requests.post("http://192.168.1.20:3030/game-complete",
      data={'teamId':teamID,
            "score":score,
            "teamName":teamName
           } #data
    ).content #req post
    )#debug