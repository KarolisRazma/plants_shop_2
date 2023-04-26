import express from 'express';
import { Position } from '../tools/database.js';
import errorTemplate from '../tools/error.js';

const router = express.Router();

router.get('/', async (req, res) => {
    let positionsArray = [];
    await Position.find({ workplaceId: req.id }).then(results => {
        if (results.length > 0) {
            res.status(200);
            for (let i = 0; i < results.length; ++i) {
                let result = results[i].toJSON();
                delete result._id;
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

router.post('/', async (req, res) => {
    let lastID = 0;
    await Position.findOne({ workplaceId: req.id }).sort({ _id: -1 }).limit(1).then(result => {
        lastID = result.toJSON().id;
    }).catch(err => {
        lastID = 0;
    });

    let overallID = 0;
    await Position.findOne().sort({ _id: -1 }).limit(1).then(result => {
        overallID = result.toJSON()._id;
    }).catch(err => {
        overallID = 0;
    });

    let position = new Position({
        _id: overallID + 1,
        id: lastID + 1,
        workplaceId: req.id,
        positionName: req.body.positionName || "",
        location: req.body.location || "",
        workTimeNorm: req.body.workTimeNorm || "",
        description: req.body.description || "",
        requirements: req.body.requirements || [],
        salary: req.body.salary || 0
    });

    if (!position.validateSync()) {
        await position.save().then(result => {
            res.status(201);
            res.location(`/workplaces/${req.params.id}/positions/${position._id}`);
            res.send(result);
        }).catch(err => {
            res.status(500);
            res.send(errorTemplate(500, 'Failed to collect data!'));
        });
    } else {
        res.status(400);
        res.send(errorTemplate(400, 'To create resource positionName is needed!'));
    }
});

router.get('/:id', async (req, res) => {
    await Position.findOne({ workplaceId: req.id, id: req.params.id }).then(result => {
        if (result !== null) {
            res.status(200);
            result = result.toJSON();
            delete result._id;
            delete result.__v;
            res.send(result);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No position found!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
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

    await Position.findOneAndUpdate({ id: req.params.id, workplaceId: req.id }, position, { new: true }).then(result => {
        if (result !== null) {
            res.status(200);
            res.location(`/workplaces/${req.id}/positions/${req.params.id}`);
            res.send(result);
        } else {
            res.status(404);
            res.send(errorTemplate(404, 'No position found for update!'));
        }
    }).catch(err => {
        res.status(500);
        res.send(errorTemplate(500, 'Failed to collect data!'));
    });
});

router.delete('/:id', async (req, res) => {
    await Position.findOneAndRemove({ workplaceId: req.id, id: req.params.id }).then(result => {
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