import express from 'express';
import { Position } from '../tools/database.js';
import errorTemplate from '../tools/error.js';

const router = express.Router();

router.get('/', async (req, res) => {
    let positionsArray = [];
    await Position.find().then(results => {
        if (results.length > 0) {
            res.status(200);
            for (let i = 0; i < results.length; ++i) {
                let result = results[i].toJSON();
                delete result.id;
                delete result.__v;
                positionsArray.push(result);
            }
            res.send(positionsArray);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No positions found!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
});

router.get('/:id', async (req, res) => {
    await Position.findOne({ _id: req.params.id }).then(result => {
        if (result !== null) {
            res.status(200);
            result = result.toJSON();
            delete result.id;
            delete result.__v;
            res.send(result);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No position found!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    })
});

router.put('/:id', async (req, res) => {
    let position = {
        positionName: req.body.positionName,
        location: req.body.location,
        workTimeNorm: req.body.workTimeNorm,
        description: req.body.description,
        requirements: req.body.requirements,
        salary: req.body.salary
    };

    await Position.findByIdAndUpdate({ _id: req.params.id }, position, { new: true }).then(result => {
        if (result !== null) {
            res.status(200);
            res.location(`/workplaces/${result.workplaceId}/positions/${result.id}`);
            res.send(result);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No position found for update!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    })
});

router.delete('/:id', async (req, res) => {
    await Position.findOneAndRemove({ _id: req.params.id }).then(result => {
        if (result) {
            res.status(204);
            res.send('');
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No position found for deletion!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
});

router.all('/', (req, res) => {
    res.status(405);
    res.send(errorTemplate(405, 'Method not allowed!'));
});

router.all('/:id', (req, res) => {
    res.status(405);
    res.send(errorTemplate(405, 'Method not allowed!'));
});

export default router;